# avatar-gen

A image generation solution built with OctoAI that will create AI generated avatar images of specific people using OctoAI's "Photo Merge" feature.

## usage

- Sign up for an OctoAI account at https://octo.ai/.  Generate an API token and update the `.env` file.

- Place at least 4 varied photos of your subject into a subfolder in the `images/<subject-name>` folder that corresponds with the subjects name.  e.g. a subject named "jim" would have example photos staged in `images/jim`<br><br>

- Update the prompt in code: https://github.com/smcdonald248/avatar-gen/blob/main/img_gen.py#L67<br><br>

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
