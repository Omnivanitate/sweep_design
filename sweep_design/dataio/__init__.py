"""The module contains simple functions for loading and saving data.

Works with next formats:
> * .txt - Methods `read_txt_file`, `write_txt_file`, `write_data`
> * .mat - Methods `read_mat_file`, `wrire_mat_file`, `write_data`

If the format is different or exсluded, then it will be enterpreted as a txt file. 

For file_name you can use both absolute path and relative path.
If you use a raltive path, then the absolut path will consist from two parts:
> first part is the default path DEFAULT_PATH from the config file from class Config,  
> second part is the relative path.

That is working to write and read.

You can change DEFAULT_PATH in config file.

If file_name is not specified for the wroten file, then the default name 
`'unnamed.(extension you chose)'` will be used for Relation instance you 
want save. If this is instance of NamedRelation you want to store, then 
the name will be `'str(instance of NamedRelation).(extension you chose)'`. 

"""

from .read.read_mat import read_mat_file as read_mat_file
from .read.read_txt import read_txt_file as read_txt_file

from .write.write_data import write_data as write_data
from .write.write_mat import write_mat_file as write_mat_file
from .write.write_txt import write_txt_file as write_txt_file
