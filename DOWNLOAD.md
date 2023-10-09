Dataset **BTAD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/T/X/In/3mAHYkWhKGOd4rU3rXGX4YKEm6m4BhFP4EU3M9N2h4pxg8gQDn2zd2DBrKTDFFqqu2bJwYtSf7TdgEBjj181piHThA8EeLT2VkvYxPIn0xp4os9Vc1ag6Zjbymoi.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='BTAD', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/thtuan/btad-beantech-anomaly-detection/download?datasetVersionNumber=1).