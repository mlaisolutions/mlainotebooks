import os
import torchvision
import torchvision.transforms as transforms
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from azureml.core import Dataset, Run
from azureml.core import Workspace, Experiment
import azureml.contrib.dataset
from azureml.contrib.dataset import FileHandlingOption, LabeledDatasetTask

#from azureml.core.authentication import InteractiveLoginAuthentication
#interactive_auth = InteractiveLoginAuthentication(tenant_id="ac5c5e7c-0141-491a-a5dd-d3608633ce62")
#workspace = Workspace.from_config()

run = Run.get_context()

# get input dataset by name
#labeled_dataset = run.input_datasets['crack_labels']
labeled_dataset = run.input_datasets['animal_labels']
#labeled_dataset = Dataset.get_by_name(workspace, 'dalatalabelproj-animals-2020-03-22 15:24:17')
#labeled_dataset = Dataset.get_by_name(workspace, 'datalabellingclass2-2020-03-28 17:15:25')


pytorch_dataset = labeled_dataset.to_torchvision()


indices = torch.randperm(len(pytorch_dataset)).tolist()
dataset_train = torch.utils.data.Subset(pytorch_dataset, indices[:24])
dataset_test = torch.utils.data.Subset(pytorch_dataset, indices[-10:])

trainloader = torch.utils.data.DataLoader(dataset_train, batch_size=1,
                                          shuffle=False, num_workers=0)

testloader = torch.utils.data.DataLoader(dataset_test, batch_size=1,
                                         shuffle=False, num_workers=0)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 5 == 4:    # print every 5 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 5))
            running_loss = 0.0

print('Finished Training')
classes = trainloader.dataset.dataset.labels
PATH = './cifar_net.pth'
torch.save(net.state_dict(), PATH)

dataiter = iter(testloader)
images, labels = dataiter.next()

net = Net()
net.load_state_dict(torch.load(PATH))

outputs = net(images)

_, predicted = torch.max(outputs, 1)

correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10 test images: %d %%' % (100 * correct / total))
pass