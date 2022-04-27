# Object Backup

This is an example program that uses the Spirit of Korth's Software Development Wrapper for Active Worlds to interact with the [Active Worlds](https://www.activeworlds.com). This program was written to showcase the ease backing up a world's objects and restoring them back their original state.

This project and/or its contributors are not affiliated with Active Worlds. 

## Usage

This program can both be used locally and through the use of the provided Docker image.

To use this program locally, you will need to have Python 3 installed. Then you can run the program with the following commands:
```bash
pip install -r requirements.txt
python ./backup
```

You can also run the program with the following command provided you have Docker installed:
```bash
docker build -t backup .
docker run -it backup
```

## License

This project is licensed under the MIT license.

## Contribution

This project is open source. Feel free to contribute to the project by opening an issue, creating a pull request, or by contacting [Johnny Irvin](mailto:irvinjohnathan@gmail.com). I appreciate any feedback or contributions. This project is not affiliated with Active Worlds, Inc. The creator of this project is not affiliated with Active Worlds, Inc.
