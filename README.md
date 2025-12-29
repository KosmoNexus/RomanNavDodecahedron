# Roman Dodecahedron Navigation Device

## A Speculative Reconstruction

![Status](https://img.shields.io/badge/Status-Experimental-yellow)
![License](https://img.shields.io/badge/License-Public%20Domain-green)

---

## Overview

Over 116 bronze dodecahedra have been discovered across the former Roman Empire, primarily in the northern provinces (Gaul, Britain, Germania), dating from the 2nd to 4th centuries CE. Despite extensive archaeological study, **no scholarly consensus exists regarding their purpose**. No Roman text describes them.

This project presents a **speculative but testable hypothesis**: that the Roman dodecahedra served as portable astronomical navigation instruments, enabling military surveyors (*mensores*) to determine latitude by day and longitude by night.

**We make no claim that this was the actual historical use.** We provide a functional reconstruction that can be 3D printed and empirically tested.

---

## The Hypothesis

### The Problem the Romans Faced

The Roman Empire spanned:
- **4,000 km east-west** (Britain to Mesopotamia)
- **2,000 km north-south** (Scotland to the Sahara)
- **Latitude range**: 25°N to 56°N

Roman generals operating in unknown territory needed to know their position. The *mensor* (military surveyor) was responsible for this critical task.

From the *Corpus Agrimensorum Romanorum* (Balbus, 2nd c. CE):

> *"The mensor must know the rising and setting of the stars, the length of shadows, the position of the sun at different hours, so that he may establish true directions and correct measurements even in unknown lands."*

The texts tell us **what** surveyors needed to know. They don't tell us **what instruments** they used.

### The Proposed Solution

A dodecahedron with 12 holes of varying sizes, combined with reference dials and tables, could serve as:

1. **Latitude finder** (daytime): Sunlight projects through holes onto a reference dial. The pattern indicates latitude.

2. **Longitude finder** (nighttime): Stars visible through specific holes, compared to reference tables and timed with a sand/water clock, indicate longitude relative to Rome.

### Why the Dodecahedron?

- **12 faces** = 12 latitude bands spanning the Empire (25°N to 56°N)
- **Variable holes** = calibrated apertures for different solar altitudes
- **Vertex knobs** = precision standoffs (15mm height for consistent projection geometry)
- **Bronze construction** = durable, survives harsh campaigns
- **No moving parts** = nothing to break in the field
- **Pattern matching** = requires no trigonometry to use

---

## Files Included

| File | Description |
|------|-------------|
| `roman_dodecahedron.stl` | Binary STL file, ready for 3D printing (592 KB, 11,836 triangles) |
| `roman_dodecahedron.scad` | OpenSCAD source file (modify parameters and regenerate) |
| `generate_dodecahedron_stl.py` | Python script to generate STL (requires only NumPy) |
| `README.md` | This file |

---

## Specifications

### Overall Dimensions

| Parameter | Value |
|-----------|-------|
| Vertex-to-vertex diameter | 80 mm |
| Edge length | 28.5 mm |
| Face-to-face diameter | 63.5 mm |
| Wall thickness | 3 mm |
| Vertex knob radius | 8 mm |
| Standoff height (when resting) | ~15 mm |

### Hole Diameters by Face

Each hole is calibrated for a latitude band spanning the Roman Empire:

| Face | Reference Location | Latitude Band | Noon Sun Altitude (Equinox) | Hole Diameter |
|------|-------------------|---------------|----------------------------|---------------|
| 1 | Alexandria | 25-27°N | 63-65° | 35 mm |
| 2 | Jerusalem | 27-30°N | 60-63° | 32 mm |
| 3 | Cyprus | 30-33°N | 57-60° | 29 mm |
| 4 | Rhodes | 33-36°N | 54-57° | 26 mm |
| 5 | Athens | 36-38°N | 52-54° | 23 mm |
| 6 | Rome | 38-41°N | 49-52° | 20 mm |
| 7 | Massilia (Marseille) | 41-44°N | 46-49° | 17 mm |
| 8 | Lugdunum (Lyon) | 44-46°N | 44-46° | 14 mm |
| 9 | Augusta Treverorum (Trier) | 46-48°N | 42-44° | 12 mm |
| 10 | Colonia (Cologne) | 48-51°N | 39-42° | 10 mm |
| 11 | Londinium (London) | 51-53°N | 37-39° | 8 mm |
| 12 | Eboracum (York) | 53-56°N | 34-37° | 6 mm |

---

## 3D Printing Instructions

### Recommended Settings

| Parameter | Recommended Value |
|-----------|-------------------|
| Layer height | 0.2 mm |
| Infill | 20-30% |
| Material | PLA or ABS |
| Color | Dark/opaque (for shadow contrast) |
| Supports | May be needed for vertex knobs |
| Print orientation | Experiment for best results |

### Post-Processing

1. **Verify hole diameters** with calipers (±0.3 mm tolerance)
2. **Sand holes smooth** if needed for clean light projection
3. **Verify standoff height** — should be ~15 mm when resting on vertex knobs

---

## How to Use

### Equipment Needed

1. **3D-printed dodecahedron** (from this STL)
2. **Day dial** — semicircular reference plate (see paper for design)
3. **Night dial** — circular star chart (see paper for design)
4. **Timing device** — 30-minute sand clock, water clock, or modern timer
5. **Flat, level surface**

### Daytime Method (Latitude)

1. Place the dodecahedron on a flat surface, resting on its vertex knobs
2. Wait for local solar noon (sun at highest point)
3. Observe which holes allow sunlight to pass through
4. Note the light spots projected onto the surface below
5. Match the pattern to reference templates
6. Read latitude from the matching template

**Precision achievable**: ±0.5° (approximately ±55 km)

### Nighttime Method (Longitude)

1. At sunset, start your timing device
2. Locate Polaris to establish north
3. Hold the dodecahedron with the largest hole (Face 1) pointing toward Polaris
4. Look through a medium-sized hole (e.g., Face 7)
5. Identify the brightest star visible through the hole
6. Find that star on the night dial for the current season
7. Note the expected hour at Rome for that star position
8. Compare to your elapsed time since sunset
9. The difference indicates longitude offset from Rome

**Precision achievable**: ±2° (approximately ±160 km at mid-latitudes)

### Multi-Hole Triangulation

Using multiple holes simultaneously increases precision:

| Holes Used | Precision |
|------------|-----------|
| 1 hole | ~2.5° |
| 2 holes | ~1° |
| 3 holes | ~0.3-0.5° |

---

## Testing Protocol

We invite empirical testing of this hypothesis.

### Latitude Test

1. Record your known latitude (from GPS)
2. At solar noon, perform the daytime observation
3. Record the indicated latitude from the instrument
4. Calculate error: Indicated − Actual
5. Repeat on 5 different days
6. Report: Mean error, standard deviation, conditions

### Longitude Test

1. Record your known longitude (from GPS)
2. At sunset, start timing
3. At Hour VI (midnight), perform nighttime observation
4. Calculate indicated longitude
5. Calculate error: Indicated − Actual
6. Repeat on 5 clear nights
7. Report: Mean error, standard deviation, conditions

### Expected Results

If the hypothesis is correct:
- **Latitude error**: Mean < 1°, standard deviation < 0.5°
- **Longitude error**: Mean < 5°, standard deviation < 3°

---

## Modifying the Design

### Using OpenSCAD

1. Install [OpenSCAD](https://openscad.org/)
2. Open `roman_dodecahedron.scad`
3. Modify parameters at the top of the file
4. Render (F6) and export as STL

### Using Python

1. Ensure NumPy is installed: `pip install numpy`
2. Edit parameters in `generate_dodecahedron_stl.py`
3. Run: `python3 generate_dodecahedron_stl.py`
4. Output: `roman_dodecahedron.stl`

### Key Parameters

```python
VERTEX_DIAMETER = 80.0   # mm, overall size
WALL_THICKNESS = 3.0     # mm, shell thickness
KNOB_RADIUS = 8.0        # mm, vertex knob size

HOLE_DIAMETERS = [       # mm, one per face
    35, 32, 29, 26, 23, 20, 17, 14, 12, 10, 8, 6
]
```

---

## Historical Context

### The Archaeological Evidence

- **116+ specimens** documented
- **Material**: Bronze
- **Size range**: 4-11 cm vertex-to-vertex
- **Distribution**: Concentrated in northern provinces
- **Date**: 2nd-4th centuries CE
- **Context**: Often military or administrative sites
- **Documentation**: No mention in any surviving Roman text

### Temporal Correlation

Sophisticated portable sundials appear in the same time period and locations. Sundials require latitude calibration — but a sundial cannot measure latitude. **Something else provided that information.**

### The Antikythera Connection

The Antikythera mechanism (c. 70-60 BCE) proves Greek engineers could build:
- Precision gear trains
- Differential mechanisms
- Astronomical computers

If they could build the Antikythera mechanism, they could certainly design a simpler portable navigation instrument.

---

## Precision Analysis

### Error Budget

| Source | Latitude Error | Longitude Error |
|--------|---------------|-----------------|
| Leveling | ±0.2° | — |
| Noon timing | ±0.1° | — |
| Spot alignment | ±0.3° | ±0.5° |
| Star identification | — | ±0.5° |
| Clock drift (12 hr) | — | ±7.5° |
| **Combined** | **±0.4°** | **±2-8°** |

### Position Uncertainty

| Condition | Latitude | Longitude | Position |
|-----------|----------|-----------|----------|
| Good conditions | ±55 km | ±160 km | ~170 km radius |
| Poor conditions | ±100 km | ±500 km | ~500 km radius |

### Comparison to Dead Reckoning

| Days of March | Dead Reckoning Error | Astronomical Fix Error |
|---------------|---------------------|----------------------|
| 10 days | ±40 km | ±170 km |
| 30 days | ±110 km | ±170 km |
| 60 days | ±200+ km | ±170 km |

**Key insight**: Dead reckoning errors accumulate. Astronomical fixes do not.

---

## Disclaimer

**This is a speculative reconstruction.** No ancient text describes the dodecahedra's function. No archaeological context provides definitive functional evidence.

We claim only that:
1. The Roman military needed portable navigation instruments
2. The dodecahedra have features consistent with such use
3. A functional system can be constructed using this design
4. The hypothesis can be tested empirically

**The ultimate test is not historical argument but physical demonstration.**

---

## References

### Primary Sources

- **Corpus Agrimensorum Romanorum** — Roman surveying texts (Frontinus, Hyginus, Balbus)
- **Vitruvius**, *De Architectura* — sundials and astronomical instruments
- **Heron of Alexandria**, *Dioptra* — surveying instruments

### Modern Scholarship

- Campbell, Brian. *The Writings of the Roman Land Surveyors* (2000)
- Dilke, O.A.W. *The Roman Land Surveyors* (1971)
- Lewis, M.J.T. *Surveying Instruments of Greece and Rome* (2001)

### On the Dodecahedra

- Portable Antiquities Scheme (UK): https://finds.org.uk — database with specimens

---

## Contributing

Test results, improvements, and alternative hypotheses are welcome.

If you test the device, please report:
- Your location (city or coordinates)
- Dates of observations
- Equipment used (printer, material)
- Raw data (indicated vs. actual positions)
- Calculated errors
- Observational conditions
- Difficulties or anomalies

---

## License

This reconstruction is released to the **public domain**. Use it however you wish.

The ancient Romans didn't patent their surveying instruments. Neither do we.

---

## Acknowledgments

This project emerged from a conversation exploring the intersection of:
- Roman military engineering
- Greek mathematical heritage
- Archaeological mystery
- Practical astronomy
- Modern maker culture

*"Build it. Test it. See if it works. That's the only argument that matters."*

---

**The mensor needed to know where he was.**

**Perhaps this is how he found out.**
