import matplotlib.pyplot as plt
import numpy as np

def create_roman_night_dial():
    # --- Setup the Polar Plot ---
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar')

    # --- 1. The Geometry (12 Sectors, 5 Rings) ---
    # 12 Holes = 12 Sectors (30 degrees each)
    theta = np.linspace(0, 2*np.pi, 13)
    
    # 5 Rings: Hours I, III, VI, IX, XII (mapped to radius 1-5)
    # Note: Hour I is outer or inner? 
    # Logic: Stars move east-to-west. The "Hour" ring represents the TIME since sunset.
    # We will map Hour I (Start of night) to the OUTER ring, moving INWARD to Hour XII? 
    # Or Inner-to-Outer? 
    # Let's use Inner=Early (I), Outer=Late (XII) for readability, 
    # but the paper implies rings indicate "Expected Hour".
    # Let's standardize: Ring 1 = Hour I, Ring 2 = Hour III, Ring 3 = Hour VI, Ring 4 = Hour IX, Ring 5 = Hour XII.
    r = [1, 2, 3, 4, 5] 
    
    # --- 2. The Data (From Table 18: Summer Stars) ---
    # Format: (Star Name, Hole_Number, Hour_Ring_Index)
    # Note: Hole 1 is North (0 deg/Top). Angles go clockwise (East) or Counter?
    # Azimuth standard: North=0, East=90.
    # We map Hole 1 -> 0 deg. Hole 4 -> 90 deg? 
    # Using Table 26 (Face Orientations):
    # Top=90 alt. Rings at 0, 72, 144...
    # For simplicity of the *Dial*, we map the 12 holes evenly to 360 degrees.
    # Sector 1 = North.
    
    star_data = [
        # Vega (Lyra)
        ("Vega", 10, 1), # Hole 10, Hour I
        ("Vega", "Center", 2), # Center? mapped to Hole 1 (Zenith) approx
        ("Vega", 1, 3), # "High" -> Near Hole 1?
        ("Vega", 7, 4), # "Low" (West?) -> Hole 7 is Westish?
        
        # Deneb (Cygnus) - Rising (East) to Setting
        ("Deneb", 11, 1), # Rising (East side)
        ("Deneb", 10, 2), # Center
        ("Deneb", 1, 3),  # High
        
        # Altair (Aquila)
        ("Altair", 9, 1), # Low
        ("Altair", 11, 2), # Rising
        ("Altair", "Center", 3),
        
        # Arcturus (Bootes) - Setting early in summer
        ("Arcturus", 8, 1), # High
        ("Arcturus", 7, 2), # Transit
        ("Arcturus", 5, 3), # Setting
        
        # Polaris (The Pivot)
        ("Polaris", 1, 0) # Fixed at Center/Hole 1
    ]

    # Helper to convert Hole # to Angle (Radians)
    # Assumes Hole 1 is Top (North), moving Clockwise?
    # Let's assume Hole 1=0deg (North), Hole 4=East, Hole 7=South, Hole 10=West
    def get_angle_for_hole(h):
        if h == "Center" or h == "High": return 0 # Zenith/North
        if isinstance(h, int):
            # Map 1-12 to 0-360 degrees (Clockwise from Top)
            # 0 is North. Matplotlib 0 is East. So we shift.
            angle_deg = (h - 1) * (360 / 12)
            # Adjust to North = Top
            return np.deg2rad(-(angle_deg - 90)) 
        return 0

    # --- 3. Plotting the Grid ---
    ax.set_theta_zero_location("N") # 0 is North
    ax.set_theta_direction(-1)      # Clockwise
    
    # Draw Sectors
    ax.set_xticks(np.deg2rad(np.arange(0, 360, 30)))
    ax.set_xticklabels([f"Hole {i}" for i in [1, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]]) 
    # Note: Hole ordering depends on your specific dodecahedron face layout.
    # This loop assumes a standard clock-face numbering for the dial sectors.

    # Draw Rings
    ax.set_yticks(r)
    ax.set_yticklabels(["Hr I", "Hr III", "Hr VI", "Hr IX", "Hr XII"])
    ax.set_ylim(0, 5.5)

    # --- 4. Plotting the Stars ---
    for star, hole, ring in star_data:
        if ring == 0: # Polaris
            ax.plot(0, 0, 'y*', markersize=20, label=star)
            continue
            
        theta_val = get_angle_for_hole(hole)
        
        # Plot Star Marker
        ax.plot(theta_val, ring, 'o', color='white', markeredgecolor='blue', markersize=10)
        
        # Add Label
        ax.text(theta_val, ring + 0.3, star, ha='center', va='bottom', fontsize=9, weight='bold')

    # --- 5. Formatting ---
    ax.set_title("ROMAN NIGHT DIAL (SUMMER)\nLatitude 41.9N (Rome) Reference", va='bottom', weight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Save
    plt.savefig("Roman_Night_Dial_Summer.pdf")
    plt.show()

create_roman_night_dial()
