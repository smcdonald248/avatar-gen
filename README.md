# avatar-gen

A image generation solution built with OctoAI that will create AI generated avatar images of specific people using OctoAI's "Photo Merge" feature.

## usage

Put at least 4 varied photos of your subject into a subfolder in the `images` folder that corresponds with the subjects name<br><br>

Update the prompt in code: https://github.com/smcdonald248/avatar-gen/blob/main/img_gen.py#L67<br><br>

```
usage: img_gen.py [-h] [-d DESCRIPTOR] subject_name

positional arguments:
  subject_name

options:
  -h, --help            show this help message and exit
  -d DESCRIPTOR, --descriptor DESCRIPTOR
                        Additional subject descriptors (e.g. gender) (Default: 'person')
```
<br>

```
python img_gen.py steve -d "man"
```
