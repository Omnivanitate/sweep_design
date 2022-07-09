"""The module contains simple functions for loading and saving data.

Works with next formats:
> * .txt - Methods: `sweep_design.dataio.read.read_txt.read_txt_file`, 
    `sweep_design.dataio.write.write_txt.write_txt_file`, 
    `sweep_design.dataio.write.write_data.write_data`
> * .mat - Methods `sweep_design.dataio.read.read_mat.read_mat_file`, 
    `sweep_design.dataio.write.write_mat.write_mat_file`, 
    `sweep_design.dataio.write.write_data.write_data`

For `sweep_design.dataio.write.write_data.write_data`, if the format is 
different or exсluded, then it will be enterpreted as a txt file. 

For `file_name` you can use both absolute path and relative path.
If you use a raltive path, then the absolut path will consist from two parts:
> first part is the default path **DEFAULT_PATH** from the config file from class 
`sweep_design.config.config.Config`,  
> second part is the relative path.

That is working to write and read.

You can change **DEFAULT_PATH** in config file.

If `file_name` is not specified for the wroten file, then the default name 
`unnamed.(extension you chose)` will be used for 
`sweep_design.math_signals.math_relation.Relation` instance you want save. 
If this is instance of  
`sweep_design.named_signals.named_relation.NamedRelation` you want to store, 
then the name will be `str(instance of NamedRelation).(extension you chose)`. 

"""

from .read.read_mat import read_mat_file as read_mat_file
from .read.read_txt import read_txt_file as read_txt_file

from .write.write_data import write_data as write_data
from .write.write_mat import write_mat_file as write_mat_file
from .write.write_txt import write_txt_file as write_txt_file
