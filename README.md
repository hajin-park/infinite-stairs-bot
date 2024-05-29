# Infinite Stairs Bot

A bot for the mobile app Infinite Stairs in Python. Two methods of
object-detection can be used; Multi-Template Matching and YOLOv10.

![Bot Example GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHZhejE3NGZ3MnN2YWNnMnVteGw2ZTJzczRseWt5YjlueGh5NTg2ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7dKdRBmjeVYzVQvinb/giphy-downsized.gif)

## Requirements

1. Enable virtualization on your device.
   [Guide](https://support.bluestacks.com/hc/en-us/articles/360058102252-How-to-enable-Virtualization-VT-on-Windows-10-for-BlueStacks-5?utm_campaign=bgp_product&utm_medium=app_player&utm_source=support#%E2%80%9CB%E2%80%9D)
2. Install BlueStacks 5 (or other emulator).
   [Download](https://www.bluestacks.com/download.html)

## Usage

1. Install
   [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
   or [miniconda](https://docs.anaconda.com/free/miniconda/)
2. Create the environment: _for Multi-Template Matching (Windows):_
    ```
    conda env create -f environment_mtm.yml
    ```
    _for YOLO (Windows):_
    ```
    conda env create -f environment_yolo.yml
    ```
3. Make sure you can activate the environment: _for Multi-Template Matching
   (Windows):_
    ```
    conda activate isb-mtm
    ```
    _for YOLO (Windows):_
    ```
    conda activate isb-yolo
    ```

## Design

The bot operates using three main components: screenshots, processing, and game
inputs. Each component is run in parallel using multiprocessing since the
processing step is by far the largest speed bottleneck.

#### Screenshots

The portion of the screen containing the game client is captured using the mss
library.

#### Processing

1. Screenshots are processed using either Multi-Template Matching or a YOLO
   model (subject to change, new models come out every several months :\\) to
   detect stair and other miscellaneous objects.
2. A path-tracing algorithm fills in any empty spaces missed by the previous
   step (max two stairs can be filled due to logical constraints).
3. Fill a queue with `True` (Turn) or `False`(Forward) values based on the path.
4. Keep track of a "current" queue state and "new" queue state. If their
   intersection is "valid" then queue new values from the "new" state into the
   "current" state

#### Game Inputs

The game will turn the character on `True` and step forward on `False`.

## Acknowledgements

Thomas, L.S.V., Gehrig, J. Multi-template matching: a versatile tool for
object-localization in microscopy images BMC Bioinformatics 21, 44 (2020).
https://doi.org/10.1186/s12859-020-3363-7
