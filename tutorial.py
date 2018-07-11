from caffe2.python import workspace, model_helper
import numpy as np

# Create random tensor of three dimensions
x = np.random.rand(4, 3, 2)
print(x)
print(x.shape)

workspace.FeedBlob("my_x", x)

x2 = workspace.FetchBlob("my_x")
print(x2)

# Create the input data
data = np.random.rand(16, 100).astype(np.float32)

# Create labels for the data as integers [0, 9].
label = (np.random.rand(16) * 10).astype(np.int32)

workspace.FeedBlob("data", data)
workspace.FeedBlob("label", label)

# Create model using a model helper
m = model_helper.ModelHelper(name="my first net")

weight = m.param_init_net.XavierFill([], 'fc_w', shape=[10, 100])
bias = m.param_init_net.ConstantFill([], 'fc_b', shape=[10, ])

fc_1 = m.net.FC(["data", "fc_w", "fc_b"], "fc1")
pred = m.net.Sigmoid(fc_1, "pred")
softmax, loss = m.net.SoftmaxWithLoss([pred, "label"], ["softmax", "loss"])

print(m.net.Proto())