from typing import Any

from furiosa.registry import Format, Metadata, Publication

from ...utils import resolve_file
from ...vision import resnet50, ssd_mobilenet, ssd_resnet34
from ...vision.yolov5 import large as yolov5l
from ...vision.yolov5 import medium as yolov5m

__all__ = [
    "ResNet50",
    "SSDMobileNet",
    "SSDResNet34",
    "YOLOv5l",
    "YOLOv5m",
    "resnet50",
    "ssd_mobilenet",
    "ssd_resnet34",
    "yolov5l",
]


_ONNX = "onnx"
_ENF = "enf"
_DFG = "dfg"


def __model_name(relative_path, truncated=True) -> str:
    if truncated:
        return f"{relative_path}_truncated"
    else:
        return relative_path


async def ResNet50(use_native_post=False, *args: Any, **kwargs: Any) -> resnet50.ResNet50Model:
    model_name = __model_name("mlcommons_resnet50_v1.5_int8", use_native_post)
    return resnet50.ResNet50Model(
        name="ResNet50",
        source=await resolve_file(model_name, _ONNX).read(),
        dfg=await resolve_file(model_name, _DFG).read(),
        enf=await resolve_file(model_name, _ENF).read(),
        format=Format.ONNX,
        family="ResNet",
        version="v1.5",
        metadata=Metadata(
            description="ResNet50 v1.5 int8 ImageNet-1K Accuracy 75.982% @ Top1",
            publication=Publication(url="https://arxiv.org/abs/1512.03385.pdf"),
        ),
        *args,
        **kwargs,
    )


# Object detection
async def SSDMobileNet(
    use_native_post=False, *args: Any, **kwargs: Any
) -> ssd_mobilenet.SSDMobileNetModel:
    model_name = __model_name("mlcommons_ssd_mobilenet_v1_int8", use_native_post)
    return ssd_mobilenet.SSDMobileNetModel(
        name="MLCommonsSSDMobileNet",
        source=await resolve_file(model_name, _ONNX).read(),
        dfg=await resolve_file(model_name, _DFG).read(),
        enf=await resolve_file(model_name, _ENF).read(),
        format=Format.ONNX,
        family="MobileNetV1",
        version="v1.1",
        metadata=Metadata(
            description="MobileNet v1 model for MLCommons v1.1",
            publication=Publication(url="https://arxiv.org/abs/1704.04861.pdf"),
        ),
        *args,
        **kwargs,
    )


async def SSDResNet34(
    use_native_post=False, *args: Any, **kwargs: Any
) -> ssd_resnet34.SSDResNet34Model:
    model_name = __model_name("mlcommons_ssd_resnet34_int8", use_native_post)
    return ssd_resnet34.SSDResNet34Model(
        name="MLCommonsSSDResNet34",
        source=await resolve_file(model_name, _ONNX).read(),
        dfg=await resolve_file(model_name, _DFG).read(),
        enf=await resolve_file(model_name, _ENF).read(),
        format=Format.ONNX,
        family="ResNet",
        version="v1.1",
        metadata=Metadata(
            description="ResNet34 model for MLCommons v1.1",
            publication=Publication(
                url="https://github.com/mlcommons/inference/tree/master/vision/classification_and_detection"  # noqa: E501
            ),
        ),
        *args,
        **kwargs,
    )


async def YOLOv5l(*args: Any, **kwargs: Any) -> yolov5l.YoloV5LargeModel:
    model_name = "yolov5l_int8"
    return yolov5l.YoloV5LargeModel(
        name="YoloV5Large",
        source=await resolve_file(model_name, _ONNX).read(),
        format=Format.ONNX,
        family="YOLOv5",
        version="v5",
        metadata=Metadata(
            description="YOLOv5 large model",
            publication=Publication(url="https://github.com/ultralytics/yolov5"),
        ),
        *args,
        **kwargs,
    )


async def YOLOv5m(use_native_post=False, *args: Any, **kwargs: Any) -> yolov5m.YoloV5MediumModel:
    model_name = "yolov5m_int8"
    return yolov5m.YoloV5MediumModel(
        name="YOLOv5Medium",
        source=await resolve_file(model_name, _ONNX).read(),
        format=Format.ONNX,
        family="YOLOv5",
        version="v5",
        metadata=Metadata(
            description="YOLOv5 medium model",
            publication=Publication(url="https://github.com/ultralytics/yolov5"),
        ),
        *args,
        **kwargs,
    )