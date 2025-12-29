import matplotlib.pyplot as plt
import numpy as np

def create_roman_day_dial():
    # --- Configuration ---
    # Nominal height of the hole center above the dial (in mm)
    # Dodecahedron Radius (~40mm) + Standoff (15mm) = 55mm approx.
    # CRITICAL: Measure your actual print height and update this value!
    HOLE_HEIGHT_MM = 55.0 
    
    # Latitude Range (Roman Empire bounds)
    latitudes = np.arange(25, 60, 5) # 25N to 55N
    
    # --- Geometry Calculations (Equinox) ---
    # At Equinox, Solar Altitude = 90 - Latitude
    # Distance r from center = h / tan(SolarAltitude)
    # r = h / tan(90 - Lat) = h * tan(Lat)
    # (As you go North, Lat increases, Sun gets lower, Shadow gets longer)
    def get_radius_for_lat(lat_deg):
        lat_rad = np.deg2rad(lat_deg)
        return HOLE_HEIGHT_MM * np.tan(lat_rad)

    # --- Plotting ---
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='polar')

    # 1. Setup Semicircle (North-facing shadow field)
    # If Sun is South, Shadows fall North.
    # We create a 180-degree fan centered on North (0 degrees).
    ax.set_theta_zero_location("N") 
    ax.set_thetamin(-90) # West
    ax.set_thetamax(90)  # East
    
    # 2. Radial Lines (Projected Face Sectors)
    # This represents the alignment lines for the spots.
    # We plot lines every 15 degrees to help alignment.
    angles = np.deg2rad(np.arange(-75, 90, 15)) 
    ax.set_xticks(angles)
    ax.set_xticklabels([]) # Clean look (no degrees)

    # 3. Latitude Arcs & Labels
    for lat in latitudes:
        r = get_radius_for_lat(lat)
        
        # Draw the Arc
        theta_range = np.linspace(-np.pi/2, np.pi/2, 100)
        ax.plot(theta_range, [r]*100, linestyle='-', color='black', alpha=0.6, linewidth=1)
        
        # Add Label (Centered)
        # We assume standard paper scale (1 unit = 1 mm is tricky in matplotlib without defining dpi)
        # Note: This plot shows RELATIVE spacing. 
        # For actual printing, ensure scaling matches the 'HOLE_HEIGHT_MM'.
        ax.text(0, r, f"{lat}°N", ha='center', va='bottom', fontsize=10, fontweight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # 4. Styling and Instructions
    ax.set_ylim(0, get_radius_for_lat(60)) # Limit to 60N (Scotland)
    ax.set_yticks([]) # Hide radial axis ticks
    
    ax.set_title(f"ROMAN DAY DIAL (EQUINOX)\nCalibrated for Hole Height: {HOLE_HEIGHT_MM}mm\nAlign Dodecahedron Center on Crosshair", va='bottom', weight='bold')
    
    # Add usage note
    plt.figtext(0.5, 0.02, 
                "INSTRUCTIONS: Place Dial on flat surface. Align North. Place Dodecahedron on vertex knobs at Center.\n"
                "At Solar Noon, rotate dial until light spot aligns with a radial line.\n"
                "Read Latitude where the center of the spot falls on the scale.\n"
                "(Valid for Equinox. For Solstices, apply Table I correction.)", 
                ha="center", fontsize=9, style='italic')

    # Grid
    ax.grid(True, linestyle=':', alpha=0.4)

    # Output
    plt.savefig("Roman_Day_Dial_Latitude.pdf")
    plt.show()

create_roman_day_dial()
