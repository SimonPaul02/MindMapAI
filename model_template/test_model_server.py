# To run this file you first have to run the server
# python model_template/model_server.py
# after that, you can run this file to test that it is working as expected.

# import grpc
import grpc
import asyncio

# import the generated classes :
import model_pb2
import model_pb2_grpc


class TestModelServicer:
    def setUp(self):
        # Add your servicer to the server
        # Replace 'YourService' with the actual service name
        self.channel = grpc.insecure_channel("localhost:8061")
        self.stub = model_pb2_grpc.ModelStub(self.channel)
        # We need to initialize this once, and not several times.
        self.predictions = self.stub.sendPrediction(model_pb2.Empty())
        self.modelID = "GPT4_turbo"

    async def test_predict(self):
        print("Testing predict")
        request = model_pb2.modelRequest(
            request='{"system" : "You are a helpful bot", "text" : [{"role" : "user", "content" : "What is 2 + 2?"}]}',
            modelID=self.modelID,
            sessionID="123",
        )
        response = self.stub.predict(request)
        print(response)
        assert response == model_pb2.Empty()
        print(self.predictions)
        try:
            print("Waiting for predictions")
            for prediction in self.predictions:
                print(prediction)
                assert prediction.sessionID == "123"
                assert type(prediction.answer) == type("str")
                break
        except Exception as e:
            print(e)
        request2 = model_pb2.modelRequest(
            request='{"system" : "You are a helpful bot", "text" : [{"role" : "user", "content" : "What is 17 + 12?"}]}',
            modelID="something Else",
            sessionID="123",
        )
        self.stub.predict(request2)
        request3 = model_pb2.modelRequest(
            request='{"system" : "You are a helpful bot", "text" : [{"role" : "user", "content" : "What is 17 + 12?"}]}',
            modelID=self.modelID,
            sessionID="123",
        )
        self.stub.predict(request3)
        try:
            print("Waiting for predictions")
            for prediction in self.predictions:
                print(prediction)
                assert prediction.sessionID == "123"
                assert type(prediction.answer) == type("str")
                break
        except Exception as e:
            print(e)

    async def test_registerModel(self):
        request = model_pb2.Empty()  # Replace with your actual request message
        response = self.stub.registerModel(request)
        # Add your assertions here
        assert response.modelID == self.modelID

    async def test_publishMetrics(self):
        request = model_pb2.metricsJson(
            modelID=self.modelID, metrics="Yeehaaw"
        )  # Replace with your actual request message
        self.stub.publishMetrics(request)
        # Wait a bit for processing...
        await asyncio.sleep(3)
        # Add your assertions here
        request = model_pb2.metricsJson(
            modelID="something Else", metrics="Yeehaaw"
        )  # Replace with your actual request message


async def test():
    test = TestModelServicer()
    test.setUp()
    await test.test_predict()
    await test.test_registerModel()
    await test.test_publishMetrics()


asyncio.run(test())
