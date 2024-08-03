import logging

import grpc
import model_handler_pb2
import model_handler_pb2_grpc


def run():
    print("calling Model Handler stub...")
    with grpc.insecure_channel("localhost:8061") as channel:
        stub = model_handler_pb2_grpc.ModelHandlerStub(channel)

        # registerModel
        stub.registerModel(
            model_handler_pb2.modelDefinition(
                needs_text=True,
                needs_image=False,
                can_text=True,
                can_image=False,
                modelID="model_1",
            )
        )

        stub.registerModel(
            model_handler_pb2.modelDefinition(
                needs_text=False,
                needs_image=True,
                can_text=False,
                can_image=True,
                modelID="model_2",
            )
        )

        stub.registerModel(
            model_handler_pb2.modelDefinition(
                needs_text=True,
                needs_image=True,
                can_text=True,
                can_image=True,
                modelID="model_3",
            )
        )

        # startTask
        stub.startTask(
            model_handler_pb2.modelRequirements(
                needs_text=True, needs_image=True, sessionID="123456789"
            )
        )

        # sendToModel
        send_to_model_response = stub.sendToModel(
            model_handler_pb2.taskRequest(request="test request", sessionID="123456789")
        )
        print("After calling the sendToModel endpoint, model handler client received: ")
        print(send_to_model_response)

        # returnToTask
        return_to_task_response = stub.returnToTask(
            model_handler_pb2.modelAnswer(answer="test answer", sessionID="123456789")
        )
        print(
            "After calling the returnToTask endpoint, model handler client received: "
        )
        print(return_to_task_response)

        # finishTask
        finish_task_response = stub.finishTask(
            model_handler_pb2.taskMetrics(metrics="test metrics", sessionID="123456789")
        )
        print("After calling the finishTask endpoint, model handler client received: ")
        print(finish_task_response)


if __name__ == "__main__":
    logging.basicConfig()
    run()
