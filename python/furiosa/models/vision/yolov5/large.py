"""Yolov5l Module

Attributes:
    CLASSES (List[str]): a list of class names
"""
__all__ = ['CLASSES', 'preprocess', 'get_anchor_per_layer_count', 'postprocess', 'YOLOv5l']

import pathlib
from typing import Any, Dict, List, Sequence

import numpy as np
import yaml

from furiosa.registry import Format, Metadata, Publication

from . import core as _yolov5
from ...model import ObjectDetectionModel
from ...utils import EXT_DFG, EXT_ENF, EXT_ONNX

with open(pathlib.Path(__file__).parent / "datasets/yolov5l/cfg.yaml", "r") as f:
    cfg = yaml.safe_load(f)
    _ANCHORS: np.array = np.float32(cfg["anchors"])
    _CLASS_NAMES: List[str] = cfg["class_names"]

_BOX_DECODER = _yolov5.boxdecoder(_CLASS_NAMES, _ANCHORS)


class YOLOv5l(ObjectDetectionModel):
    """YOLOv5 Large model"""

    @classmethod
    def get_artifact_name(cls):
        return "yolov5l_int8"

    @classmethod
    def load_aux(cls, artifacts: Dict[str, bytes], *args, **kwargs):
        return cls(
            name="YoloV5Large",
            source=artifacts[EXT_ONNX],
            dfg=artifacts[EXT_DFG],
            enf=artifacts[EXT_ENF],
            format=Format.ONNX,
            family="YOLOv5",
            version="v5",
            compiler_config={
                "without_quantize": {
                    "parameters": [
                        {
                            "permute": [0, 2, 3, 1],
                        }
                    ]
                }
            },
            metadata=Metadata(
                description="YOLOv5 large model",
                publication=Publication(url="https://github.com/ultralytics/yolov5"),
            ),
            *args,
            **kwargs,
        )


def get_anchor_per_layer_count() -> int:
    """Anchors per layers

    Returns:
        int: the number of anchors for yolov5l
    """
    return _ANCHORS.shape[1]


CLASSES: List[str] = _CLASS_NAMES
preprocess = _yolov5.preprocess


def postprocess(
    batch_feats: Sequence[np.array],
    batch_preproc_param: Sequence[Dict[str, Any]],
    conf_thres: float = 0.25,
    iou_thres: float = 0.45,
) -> List[List[_yolov5.ObjectDetectionResult]]:
    """Yolov5l Postprocess.

    Args:
        batch_feats (Sequence[np.array]): P3/8, P4/16, P5/32 features from yolov5l model.
        batch_preproc_param (Dict[str, Any]): A configuration for each image generated by the preprocessor.
            For example, it could be the reduction ratio of the image, the actual image width and height.
        conf_threshold (float, optional): Confidence score threshold. The default to 0.25
        iou_thres (float, optional): IoU threshold value for the NMS processing. The default to 0.45.

    Returns:
        yolov5.ObjectDetectionResult: Detected Bounding Box and its score and label by Yolov5l.
    """
    return _yolov5.postprocess(
        batch_feats,
        _BOX_DECODER,
        get_anchor_per_layer_count(),
        _CLASS_NAMES,
        batch_preproc_param,
        conf_thres=conf_thres,
        iou_thres=iou_thres,
    )
