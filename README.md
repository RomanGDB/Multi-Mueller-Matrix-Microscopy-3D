# Mueller Matrix Microscopy

## Summary

Polarization is a fundamental property of light that can be modeled using four real numbers known as the Stokes parameters. When light interacts with an object, its polarization state is transformed through a transfer function known as the Mueller matrix. This matrix fully describes the polarimetric properties of the object, which are directly associated with its physical properties, mainly of a mechanical nature. In recent years, Mueller polarimetric imaging has emerged: a technique capable of measuring Mueller matrices over a bounded field of view, allowing visualization of such physical characteristics on a two-dimensional map.

## Materials and Methodology

<pre>
<p align="center">
<img src="https://github.com/user-attachments/assets/9980bfc1-0515-4bea-8e9e-1b88e3ccab17" alt="Figure 1" width="500"/>
</p>
<p align="center"><b>Figure 1:</b> System diagram.</p>
</pre>

The designed system consists of a set of 3D-printed parts and optical components that form a Mueller matrix microscope for research and laboratory use. The illumination is provided by an LED (ThorLabs M405LP1) mounted inside a housing, along with two lenses used as a collector and a condenser, and a motorized linear polarizer driven by a stepper motor (BYJ48) controlled by a Raspberry Pi. The sample is placed on a 3D-printed stage, attached to a manual XYZ stage. A microscope objective captures the light diffracted by the sample, which is projected onto a polarized sensor (BFS-U3-51S5P-C) through a tube lens, which in our case is an electrical lens [model]. To reduce the overall height of the system, a mirror was incorporated between the objective and the camera, redirecting the light beam without compromising image quality (see Fig. 1).

To measure the polarimetric parameters, we follow the following procedure. The illuminator's polarizer (generator) is rotated at four different angles: 0º, 45º, 90º, and 135º. For each of these generator polarization states, four images are recorded by the camera corresponding to the I₀, I₄₅, I₉₀, and I₁₃₅ states, resulting from measuring the diffracted light with an analyzer oriented at those same angles. In total, 16 images are obtained, which are organized into a 4×4 intensity matrix (see Fig. 2.a). Based on the Stokes formalism [1], the input Stokes vectors corresponding to each generator angle are calculated. This provides four input polarization states and four output polarization states. With this information, a 3×3 Mueller matrix representing the linear relationship between the input and output Stokes parameters can be robustly estimated (see Fig. 2.b). Finally, using a variant of the Lu-Chipman decomposition algorithm proposed by Swami [2], three fundamental polarimetric properties are extracted: linear diattenuation, linear retardance, and  power of depolarization (see Fig. 2.c).

<pre>
<p align="center">
<img src="https://github.com/user-attachments/assets/c3d254d9-ee3a-4968-9531-9013a7df6b32" alt="Figure 2" width="1000"/>
a)                                     b)                                     c)
</p>  
<p align="center"><b>Figure 2:</b> Imaging acquisition scheme.</p>
</pre>

## Installation

1) Install Visual C++  
https://www.microsoft.com/es-es/download/details.aspx?id=48145  
3) Download and install Python 3.10  
https://www.python.org/downloads/  
5) Download and install Visual Code Studio (VCS)  
https://code.visualstudio.com/  
7) Download and install 'Git for Windows' from VCS  
8) Clone github  
https://github.com/RomanGDB/Mueller-Matrix-Microscopy/edit/main/  
10) Install Spinnaker SDK  
https://www.teledynevisionsolutions.com/products/spinnaker-sdk/?model=Spinnaker%20SDK&vertical=machine%20vision&segment=iis  
11) Install libraries  
numpy opencv-python simple-pyspin PyQt5 paramiko  
12) If using electrical lens  
Install Drivers https://www.optotune.com/downloads  
pip install git+https://github.com/OrganicIrradiation/opto.git  

## References

[1] Dennis H. Goldstein, *Polarized Light*, 3rd edition, CRC Press, 2010.  
[2] Mahesh K. Swami et al., *Polar decomposition of 3×3 Mueller matrix: a tool for quantitative tissue polarimetry*, Optics Express, 2006.

## Related Publications

Roman Demczylo & Ariel Fernández, *Single-shot 3×3 Mueller matrix microscopy with color polarization encoding*, Optics Letters, 2024.  
Roman Demczylo, Diego Silva, Federico Lecumberry, Ariel Fernández, *Field of view extension in Mueller matrix microscopy for whole-slide imaging of biological samples*, Results in Optics, 2025.


## Contact

Feel free to contact me at my personal email:  
roman.demczylo@gmail.com
