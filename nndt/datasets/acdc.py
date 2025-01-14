from nndt.datasets.dataset import dataset


class ACDC(dataset):
    def __init__(self, name='ACDC_5', to_path=None):
        super().__init__()

        __dict = {
            'ACDC_5': [
                ['https://drive.google.com/file/d/1wOYib-CBGcx_x-ap0eBu6mstHbICLxKG/view?usp=sharing',
                 'https://www.dropbox.com/s/m4mz82s5cyotcva/ACDC_5.zip?raw=1'],
                '877684e505bf97c3a31cb4876f79e862'

            ],
            'wrong_url_test': [
                ['https://drive.google.com/file',
                 'a',
                 'b',
                 'https://a',
                 'https://www.dropbox.com/s/m'],
                '877684e505bf97c3a31cb4876f79e862'

            ],
            'wrong_hash_test': [
                ['https://drive.google.com/file/d/1wOYib-CBGcx_x-ap0eBu6mstHbICLxKG/view?usp=sharing',
                 'https://www.dropbox.com/s/m4mz82s5cyotcva/ACDC_5.zip?raw=1'],
                '877684e505bf97c3a31cb4876f79e862  '],
            'dropbox_test': [
                ['https://www.dropbox.com/s/m4mz82s5cyotcva/ACDC_5.zip?raw=1'],
                '877684e505bf97c3a31cb4876f79e862'
            ]
        }

        if name in __dict.keys():
            if 'test' in name:
                self.name = 'ACDC_5'
            else:
                self.name = name
            self.to_path = to_path
            self.urls, self.hash = __dict[name]
        else:
            raise ValueError(f'name must be in {[key for key in __dict if "test" not in key]}')

    def load(self):
        super(ACDC, self).load()
