class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
                               #color channel, # of conv layers
        self.conv1 = nn.Conv2d(in_channels= 1, out_channels= 32, kernel_size= 3)
        self.maxpool = nn.MaxPool2d(kernel_size= 2, stride= 2)
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.neurons = self.linear_input_neurons()

        self.fc1 = nn.Linear(self.linear_input_neurons(), 1000)
        self.fc2 = nn.Linear(1000, 500)
        self.fc3 = nn.Linear(500, classes)

    def forward(self, x):
        x = self.maxpool(F.relu(self.conv1(x.float())))
        x = self.maxpool(F.relu(self.conv2(x.float())))
        x = x.view(-1, self.neurons)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)


        return x
        # here we apply convolution operations before linear layer, and it returns the 4-dimensional size tensor. 
	    def size_after_relu(self, x):
	        x = self.maxpool(F.relu(self.conv1(x.float())))
	        x = self.maxpool(F.relu(self.conv2(x.float())))
	
	        return x.size()
	
	
	    # after obtaining the size in above method, we call it and multiply all elements of the returned size.
	    def linear_input_neurons(self):
	        size = self.size_after_relu(torch.rand(1, 1, 64, 32)) # image size: 64x32
	        m = 1
	        for i in size:
	            m *= i
	
        return int(m)