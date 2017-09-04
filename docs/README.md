## Introduction

The overaching goals of our work are to:

*    distinguish the features of the placental chorionic surface vascular network which are associated with increased risk of Autism Spectrum Disorder (ASD), and

*    explore the effect of these features on function, in particular on oxygen transfer efficiency.

Please see (cite article here) for the full discussion.

As a prerequisite to our first aim, we must extract the vascular network structure from photo images of the placenta.  The images here are taken either at delivery or upon pathological evaluation and are noisy due to the complexity and variation of the tissue itself (e.g. as compared to retinal vessels, say), as well as to the variation in photographic equiment, lighting, etc.  Manual extraction of the vascular network is time-consuming and expensive.  Thus, our goal here is to

*    improve the automatic extraction of the vascular network structure. 

The following is the documentation of the code for this imaging portion of our project.
 

## Data Pre-processing

### National Children's Study (NCS) Dataset

The National Children's Study (NCS) consists participants assumed to be representative of the general population, with unknown risk for autism.  The placentas were photographed and the vasculature manually traced using consistent protocols described in [1](#ref-1). We received photographs of placentas already processed to remove glare and/or increase contrast. Thus, we begin with pairs of images of photos and traces for each placenta as shown below.

<img align="center" src="img/preprocessing_raw_photo.png" height="150" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png" height="150" alt=""  class="inline"/>  <img align="center" src="img/preprocessing_raw_trace.png" height="150" alt="hi" class="inline"/> 

The first step is to adjust the background, crop, and convert the trace to black and white, using the script [`data.setup.initial.py`](https://github.com/canghel/placenta/blob/master/scripts/data.setup.initial.py ).

<img align="center" src="img/preprocessing_white_and_crop_photo.png" height="150" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="150" alt="" class="inline"/>  <img align="center" src="img/preprocessing_white_and_crop_trace.png" height="150" alt="hi" class="inline"/> 

We crop both images into non-overlapping squares of 256 by 256 pixels, to be passed into the neural network. The salient feature of the images is the vasculature, which does not have an up-down or left-right orientation. Thus we augment the training dataset by rotating the images by 0&deg;, 90&deg;, 180&deg; and 270&deg;. An internal option to the neural network also flips them horizontally.  The function to crop and rotate the images is [`cropandrotate.m`](https://github.com/canghel/placenta/blob/master/scripts/cropandrotate.m).  

<img align="center" src="img/preprocessing_crop_photo_Angle_0.png" height="75" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="75" alt="" class="inline"/>  <img align="center" src="img/preprocessing_crop_photo_Angle_90.png" height="75" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="75" alt="" class="inline"/>  <img align="center" src="img/preprocessing_crop_photo_Angle_180.png" height="75" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="75" alt="" class="inline"/>  <img align="center" src="img/preprocessing_crop_photo_Angle_270.png" height="75" alt="hi" class="inline"/> \\
<img align="center" src="img/preprocessing_crop_trace_Angle_0.png" height="75" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="75" alt="" class="inline"/>  <img align="center" src="img/preprocessing_crop_trace_Angle_90.png" height="75" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="75" alt="" class="inline"/>  <img align="center" src="img/preprocessing_crop_trace_Angle_180.png" height="75" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="75" alt="" class="inline"/>  <img align="center" src="img/preprocessing_crop_trace_Angle_270.png" height="75" alt="hi" class="inline"/> 

## References 

1. <a id="ref-1"></a> J.-M. Chang, H. Zeng, R. Han, Y.-M. Chang, R. Shah, C. Salafia, C. Newschaffer, R. Miller, P. Katzman, J. Moye, M. Fallin, C. Walker, L. Croen, "Autism risk classification using placental chorionic surface vascular network features," _Accepted for publication in BMC Medical Informatics and Decision Making_, July 2017.  

## Software Specifications

For preprocessing, we used the following:

*	Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32

*   MATLAB (version, etc.)

## Authors

The imaging portion of the project was led by Jen-Mei Chang, Karamatou (Kara) Yacoubou Djima, and Catalina Anghel, with Kellie Archer, Amy Cochran, Anca Radulescu, Rebecca Turner, Lan Zhong and with the support of developmental pathologist Dr. Carolyn Salafia.

(Other authors as well, involved in data collection?)

## Acknowledgements

We gratefully acknowledge the support of the following organizations and persons.  

*	The project was part of the [MBI Women Advancing Mathematical Biology: Understanding Complex Biological Systems with Mathematics 2017 Workshop](https://mbi.osu.edu/event/?id=1067 ).  The Mathematical Biosciences Institute sponsored the workshop, with support from Association for Women in Mathematics, The Society for Mathematical Biology, and Microsoft Research.

*   We received biology expertise and data support from Dr. Carolyn Salafia, Ruchit Shah, Dr. George Merz, and Dr. Richard K. Miller.

*	We thank the medical professionals involved in the National Children's Study (NCS), and most importantly the participants who donated their placentas.


<!-- ```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/canghel/placenta/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out. -->
