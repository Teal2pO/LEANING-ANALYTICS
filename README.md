<div style="display: flex; justify-content: space-between;">
  <img src="assets/teal_logo.jpeg" width="300" />
  <img src="assets/erasmus_logoW.png" width="300" /> 
</div>

<br>

# TEAL Learning Resource Management

## Overview

This is the source code for the TEAL2.O Learning Analytics application. This application provides learning anaytics for the classroom Moodle to facilitate the quality assurance process.


## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact Information](#contact-information)

## Getting Started

### Prerequisites

TEAL Learning Analytics is a Python web application built on Plotly Dash and Flask frameworks. Please ensure that you have Python 3 installed on your system. You can use the following commands to install Python on Ubuntu

```
sudo apt-get update
sudo apt-get install python3
```


### Dependencies

The application relies on the following Python packages. Make sure to install the specified versions for compatibility.

- **dash** (version 2.6.1)
- **dash_bootstrap_components** (version 1.1.0)
- **Flask** (version 2.2.2)
- **Flask_RESTful** (version 0.3.9)
- **mysql_connector_repackaged** (version 0.3.1)
- **networkx** (version 3.2.1)
- **numpy** (version 1.22.3)
- **pandas** (version 1.4.2)
- **plotly** (version 5.8.0)
- **PyGithub** (version 2.1.1)
- **pytz** (version 2019.3)
- **requests** (version 2.22.0)
- **scikit_learn** (version 1.3.2)
- **SQLAlchemy** (version 1.2.19)
- **urllib3** (version 1.25.8)
- **xmltodict** (version 0.13.0)


To install the required dependencies, you can use the following command.

```
pip install -r requirements.txt
```

### Deployment

Since this is a web application, consider deploying it using Gunicorn. You can create a service file on Ubuntu to establish a WebSocket and enable web access by configuring Nginx as a reverse proxy.


### Configuration
Duplicate the `serverConfig_sample.py` file and rename the copy to `serverConfig.py`. Once copied, open `serverConfig.py` and update the server URLs and Moodle API token to establish a connections. 

## Usage
For detailed instructions on how to use TEAL, please refer to the guides available on the official TEAL website: https://teal.cs.ait.ac.th.
 Currenty the TEAL platform is hosted at https://teal2o.pdn.ac.lk.


## Contributing

We welcome contributions! To contribute, fork the repository and create a new branch.
Make your changes and test them thoroughly.
Submit a pull request, providing a detailed description of the changes.


### Current Contributors

<div style="display: flex; align-items: center; margin-bottom: 10px;margin-left: 20px;">
  <img src="https://github.com/nrnw.png" width="50" style="border-radius: 50%; margin-right: 10px;">
  <span><strong><a href="https://github.com/nrnw">Niuru Ranaweera</a></strong></span>
</div>

<div style="display: flex; align-items: center; margin-bottom: 10px;margin-left: 20px;">
  <img src="https://github.com/mugalan.png" width="50" style="border-radius: 50%; margin-right: 10px;">
  <span><strong><a href="https://github.com/mugalan">Sanjeeva Maithripala</a></strong></span>
</div>

<div style="display: flex; align-items: center; margin-bottom: 10px;margin-left: 20px;">
  <img src="https://github.com/thilankarx.png" width="50" style="border-radius: 50%; margin-right: 10px;">
  <span><strong><a href="https://github.com/thilankarx">Thilanka Gunarathne</a></strong></span>
</div>

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


## Acknowledgments
We would like to express our gratitude to the the European Union and Erasmus+ for their funding support, enabling the realization of this project.


## Contact Information
Please contact the nearest TEAL Support and Development Center (SDC) to obtain access or for more information through https://teal2o.pdn.ac.lk/index/sdc.html
