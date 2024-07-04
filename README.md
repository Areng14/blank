# Blank

A goofy image format using only whitespace.

## Overview

`blank` goofy ahh file format where it only uses whitespace.

##Datastructure
.blank files are text files that use whitespace to represent pixel values. Each pixel is stored as follows:

```[SPACE][TAB][SPACE][TAB]```
Each increment of whitespace corresponds to an increment in the RGB values, and the format is as follows:

Red (R): Represented by the number of spaces before the first tab.
Green (G): Represented by the number of spaces before the second tab.
Blue (B): Represented by the number of spaces before the third tab.
Encoding Format
For example, a white pixel (255, 255, 255) would be stored as:

```[255 spaces][TAB][255 spaces][TAB][255 spaces][TAB]```

Each row of pixels ends with a newline character.

## Features

- Encode images to `.blank` format using whitespace.
- Decode `.blank` files back to standard image formats.
- Optional resizing during encoding to reduce file size.
- Supports PNG, JPEG, and `.blank` file formats.
- Automatically opens decoded images in the default image viewer.

## Installation

Download the zip file from the releases tab, Then

### To encrypt
Open a .png, .jpg, .jpeg with blank.exe
The output is a [FILENAME].blank

### To decrypt
Open a .blank with blank.exe
The output is [FILENAME].png
