## Paragraph Segmentation

This repostiory revolves around the logic which I used for segmentation of paragrph within a doument's page using the same logic of edge detection in image processing. 
In image processing, first order derivative as well as 2nd order derivatie, both are used for edge detection depending on the type of noise present in the image. 1st order derivative is very sensative to noises. Though 2nd order derivative is also sensetive to the noise, it can easily detect a zero crossing, ramp, step.

Both of the derivatives are used to detect the changes in the intensity and according to that, edge is detected. 

**To get a better insight of how edge in an image is detected, go to the logic folder and have a look at the ppts**

Before proceeding further, I have assumed that you have parsed the pdf document and have extrated useful features from itinto a datframe.
To detect the paragraph, I have used the distance between the lines of the document.

**To have a better insight of the dataframe check the documnet folder. Also check the graphs folder to understand the distribution of the lines along the page**

Rest of the information and steps have been explained in the .py itself. 

*I will update this Readme again if you have any confusing understaing this. Please contact for 
any doubdt or confusin***
