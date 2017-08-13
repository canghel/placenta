## Introduction

The following is the documentation of the code for the imaging portion of our project.

For a full discussion of  please see, please see (cite article here).
 
<!-- You can use the [editor on GitHub](https://github.com/canghel/placenta/edit/master/docs/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files. -->

## Data pre-processing

### National Children's Study (NCS) Dataset

The raw placenta images we began with are pairs of photos and manually traced arteries and veins for each placenta.

<img align="center" src="img/preprocessing_raw_photo.png" height="150" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png" height="150" alt=""  class="inline"/>  <img align="center" src="img/preprocessing_raw_trace.png" height="150" alt="hi" class="inline"/> 

The first step is to adjust the background, crop, and convert the trace to black and white, using the script [`data.setup.initial.py`](https://github.com/canghel/placenta/blob/master/scripts/data.setup.initial.py ).

<img align="center" src="img/preprocessing_white_and_crop_photo.png" height="150" alt="hi" class="inline"/> <img align="center" src="img/whitespace.png"  height="150" alt="" class="inline"/>  <img align="center" src="img/preprocessing_white_and_crop_trace.png" height="150" alt="hi" class="inline"/> 

## Software Specifications

For preprocessing, we used the following:

*	Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
*   MATLAB (version, etc.)

## Authors

The imaging portion of the project was led by Jen-Mei Chang, Karamatou (Kara) Yacoubou Djima, and Catalina Anghel, with 
Kellie Archer, Amy Cochran, Anca Radulescu, Rebecca Turner, Lan Zhong and with the support of developmental pathologist Dr. Carolyn Salafia.

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
