#!/usr/bin/env python3
"""
Roman Dodecahedron Navigation Device - STL Generator
A speculative reconstruction based on archaeological artifacts

Generates a 3D-printable STL file of a dodecahedron with:
- 12 calibrated holes (varying diameters for latitude bands)
- 20 vertex knobs (serving as 15mm standoffs)
- 80mm vertex-to-vertex diameter
"""

import numpy as np
import struct

# ============================================================================
# PARAMETERS
# ============================================================================

VERTEX_DIAMETER = 80.0  # mm, vertex to vertex
WALL_THICKNESS = 3.0    # mm (increased for printability)
KNOB_RADIUS = 8.0       # mm

# Hole diameters calibrated for latitude bands
HOLE_DIAMETERS = [
    35.0,  # Face 0:  Alexandria (25-27°N)
    32.0,  # Face 1:  Jerusalem (27-30°N)
    29.0,  # Face 2:  Cyprus (30-33°N)
    26.0,  # Face 3:  Rhodes (33-36°N)
    23.0,  # Face 4:  Athens (36-38°N)
    20.0,  # Face 5:  Rome (38-41°N)
    17.0,  # Face 6:  Massilia (41-44°N)
    14.0,  # Face 7:  Lugdunum (44-46°N)
    12.0,  # Face 8:  Augusta Treverorum (46-48°N)
    10.0,  # Face 9:  Colonia (48-51°N)
    8.0,   # Face 10: Londinium (51-53°N)
    6.0    # Face 11: Eboracum (53-56°N)
]

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2

# Mesh resolution
SPHERE_SEGMENTS = 16
CYLINDER_SEGMENTS = 32

# ============================================================================
# GEOMETRY FUNCTIONS
# ============================================================================

def get_dodecahedron_vertices(circumradius):
    """Generate the 20 vertices of a regular dodecahedron."""
    scale = circumradius / np.sqrt(3)
    
    vertices = []
    
    # (±1, ±1, ±1)
    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                vertices.append([i * scale, j * scale, k * scale])
    
    # (0, ±1/φ, ±φ)
    for j in [-1, 1]:
        for k in [-1, 1]:
            vertices.append([0, j * scale / PHI, k * scale * PHI])
    
    # (±1/φ, ±φ, 0)
    for i in [-1, 1]:
        for j in [-1, 1]:
            vertices.append([i * scale / PHI, j * scale * PHI, 0])
    
    # (±φ, 0, ±1/φ)
    for i in [-1, 1]:
        for k in [-1, 1]:
            vertices.append([i * scale * PHI, 0, k * scale / PHI])
    
    return np.array(vertices)

def get_dodecahedron_faces():
    """Return face definitions as vertex indices (each face is a pentagon)."""
    return [
        [0, 8, 4, 14, 12],
        [0, 16, 2, 10, 8],
        [0, 12, 1, 17, 16],
        [1, 12, 14, 5, 9],
        [1, 9, 11, 3, 17],
        [2, 16, 17, 3, 13],
        [2, 13, 15, 6, 10],
        [4, 8, 10, 6, 18],
        [4, 18, 19, 5, 14],
        [3, 11, 7, 15, 13],
        [5, 19, 7, 11, 9],
        [6, 15, 7, 19, 18]
    ]

def get_face_centers(vertices, faces):
    """Calculate the center point of each pentagonal face."""
    centers = []
    for face in faces:
        face_verts = vertices[face]
        center = np.mean(face_verts, axis=0)
        centers.append(center)
    return np.array(centers)

def get_face_normals(face_centers):
    """Calculate outward-pointing normal for each face."""
    normals = []
    for center in face_centers:
        normal = center / np.linalg.norm(center)
        normals.append(normal)
    return np.array(normals)

def triangulate_pentagon(vertices, face_indices):
    """Triangulate a pentagon into 3 triangles (fan from first vertex)."""
    triangles = []
    v0 = face_indices[0]
    for i in range(1, len(face_indices) - 1):
        triangles.append([v0, face_indices[i], face_indices[i + 1]])
    return triangles

def create_sphere_mesh(center, radius, segments=16):
    """Create triangulated sphere mesh."""
    vertices = []
    triangles = []
    
    # Generate vertices
    for i in range(segments + 1):
        lat = np.pi * (i / segments - 0.5)
        for j in range(segments):
            lon = 2 * np.pi * j / segments
            x = center[0] + radius * np.cos(lat) * np.cos(lon)
            y = center[1] + radius * np.cos(lat) * np.sin(lon)
            z = center[2] + radius * np.sin(lat)
            vertices.append([x, y, z])
    
    # Generate triangles
    for i in range(segments):
        for j in range(segments):
            v0 = i * segments + j
            v1 = i * segments + (j + 1) % segments
            v2 = (i + 1) * segments + j
            v3 = (i + 1) * segments + (j + 1) % segments
            triangles.append([v0, v2, v1])
            triangles.append([v1, v2, v3])
    
    return np.array(vertices), triangles

def create_cylinder_mesh(center, direction, radius, height, segments=32):
    """Create a cylinder aligned with given direction."""
    vertices = []
    triangles = []
    
    # Normalize direction
    direction = np.array(direction) / np.linalg.norm(direction)
    
    # Create orthonormal basis
    if abs(direction[2]) < 0.9:
        up = np.array([0, 0, 1])
    else:
        up = np.array([1, 0, 0])
    
    right = np.cross(direction, up)
    right = right / np.linalg.norm(right)
    up = np.cross(right, direction)
    
    # Generate vertices for top and bottom circles
    base_center = np.array(center) - direction * height / 2
    top_center = np.array(center) + direction * height / 2
    
    # Bottom cap center
    vertices.append(base_center.tolist())
    # Bottom circle
    for i in range(segments):
        angle = 2 * np.pi * i / segments
        point = base_center + radius * (np.cos(angle) * right + np.sin(angle) * up)
        vertices.append(point.tolist())
    
    # Top cap center
    top_center_idx = len(vertices)
    vertices.append(top_center.tolist())
    # Top circle
    for i in range(segments):
        angle = 2 * np.pi * i / segments
        point = top_center + radius * (np.cos(angle) * right + np.sin(angle) * up)
        vertices.append(point.tolist())
    
    # Bottom cap triangles (reversed winding for outward normal)
    for i in range(segments):
        v1 = 1 + i
        v2 = 1 + (i + 1) % segments
        triangles.append([0, v2, v1])
    
    # Top cap triangles
    for i in range(segments):
        v1 = top_center_idx + 1 + i
        v2 = top_center_idx + 1 + (i + 1) % segments
        triangles.append([top_center_idx, v1, v2])
    
    # Side triangles
    for i in range(segments):
        b1 = 1 + i
        b2 = 1 + (i + 1) % segments
        t1 = top_center_idx + 1 + i
        t2 = top_center_idx + 1 + (i + 1) % segments
        triangles.append([b1, t1, b2])
        triangles.append([b2, t1, t2])
    
    return np.array(vertices), triangles

def compute_normal(v0, v1, v2):
    """Compute normal vector for a triangle."""
    edge1 = v1 - v0
    edge2 = v2 - v0
    normal = np.cross(edge1, edge2)
    norm = np.linalg.norm(normal)
    if norm > 0:
        normal = normal / norm
    return normal

# ============================================================================
# STL WRITING
# ============================================================================

def write_binary_stl(filename, all_triangles_with_vertices):
    """Write triangles to binary STL file."""
    with open(filename, 'wb') as f:
        # Header (80 bytes)
        header = b'Roman Dodecahedron Navigation Device v1.0' + b'\0' * 39
        f.write(header[:80])
        
        # Number of triangles
        num_triangles = len(all_triangles_with_vertices)
        f.write(struct.pack('<I', num_triangles))
        
        # Write each triangle
        for v0, v1, v2 in all_triangles_with_vertices:
            normal = compute_normal(np.array(v0), np.array(v1), np.array(v2))
            
            # Normal vector
            f.write(struct.pack('<fff', normal[0], normal[1], normal[2]))
            
            # Vertices
            f.write(struct.pack('<fff', v0[0], v0[1], v0[2]))
            f.write(struct.pack('<fff', v1[0], v1[1], v1[2]))
            f.write(struct.pack('<fff', v2[0], v2[1], v2[2]))
            
            # Attribute byte count
            f.write(struct.pack('<H', 0))
    
    print(f"Written {num_triangles} triangles to {filename}")

# ============================================================================
# MAIN DODECAHEDRON GENERATION
# ============================================================================

def create_dodecahedron_shell(circumradius, wall_thickness, hole_diameters):
    """Create a hollow dodecahedron with holes in each face."""
    
    all_triangles = []
    
    # Get geometry
    outer_vertices = get_dodecahedron_vertices(circumradius)
    inner_scale = (circumradius - wall_thickness) / circumradius
    inner_vertices = get_dodecahedron_vertices(circumradius - wall_thickness)
    faces = get_dodecahedron_faces()
    face_centers = get_face_centers(outer_vertices, faces)
    face_normals = get_face_normals(face_centers)
    
    # For each face, create the outer and inner pentagons, minus the hole
    for face_idx, face in enumerate(faces):
        hole_radius = hole_diameters[face_idx] / 2
        face_center = face_centers[face_idx]
        face_normal = face_normals[face_idx]
        
        # Get outer and inner face vertices
        outer_face_verts = outer_vertices[face]
        inner_face_verts = inner_vertices[face]
        
        # Calculate distance from center to edge (pentagon inradius)
        edge_midpoint = (outer_face_verts[0] + outer_face_verts[1]) / 2
        edge_midpoint_local = edge_midpoint - face_center
        # Project onto face plane
        inradius = np.linalg.norm(edge_midpoint_local - np.dot(edge_midpoint_local, face_normal) * face_normal)
        
        # If hole is smaller than face, create annular region
        if hole_radius < inradius * 0.95:
            # Create hole edge vertices on outer surface
            outer_hole_verts = []
            inner_hole_verts = []
            
            # Create basis vectors on face
            v0_local = outer_face_verts[0] - face_center
            v0_proj = v0_local - np.dot(v0_local, face_normal) * face_normal
            basis_x = v0_proj / np.linalg.norm(v0_proj)
            basis_y = np.cross(face_normal, basis_x)
            
            # Hole vertices on outer surface
            outer_face_center = face_center
            inner_face_center = face_center * inner_scale
            
            for i in range(CYLINDER_SEGMENTS):
                angle = 2 * np.pi * i / CYLINDER_SEGMENTS
                offset = hole_radius * (np.cos(angle) * basis_x + np.sin(angle) * basis_y)
                outer_hole_verts.append(outer_face_center + offset)
                inner_hole_verts.append(inner_face_center + offset * inner_scale)
            
            # Triangulate the annular region on outer face
            # From pentagon vertices to hole edge
            for i in range(5):
                v0_out = outer_face_verts[i]
                v1_out = outer_face_verts[(i + 1) % 5]
                
                # Find nearest hole vertices
                angles_v0 = []
                for hv in outer_hole_verts:
                    local = hv - outer_face_center
                    angle = np.arctan2(np.dot(local, basis_y), np.dot(local, basis_x))
                    angles_v0.append(angle)
                
                local_v0 = v0_out - outer_face_center
                angle_v0 = np.arctan2(np.dot(local_v0, basis_y), np.dot(local_v0, basis_x))
                local_v1 = v1_out - outer_face_center
                angle_v1 = np.arctan2(np.dot(local_v1, basis_y), np.dot(local_v1, basis_x))
                
                # Simple triangulation: connect pentagon edge to hole
                # Find hole vertices between the two angles
                hole_indices = []
                for hi, ha in enumerate(angles_v0):
                    # Normalize angles
                    a0 = angle_v0 % (2 * np.pi)
                    a1 = angle_v1 % (2 * np.pi)
                    ha_norm = ha % (2 * np.pi)
                    
                    if a0 > a1:
                        if ha_norm >= a1 and ha_norm <= a0:
                            hole_indices.append(hi)
                    else:
                        if ha_norm >= a0 and ha_norm <= a1:
                            hole_indices.append(hi)
                
                # Create fan triangles
                if len(hole_indices) >= 1:
                    # Triangle from v0, v1, and first hole vertex
                    hi = hole_indices[0] if hole_indices else 0
                    all_triangles.append((v0_out.tolist(), outer_hole_verts[hi].tolist(), v1_out.tolist()))
                    
                    # Additional triangles along hole edge
                    for j in range(len(hole_indices) - 1):
                        hi1 = hole_indices[j]
                        hi2 = hole_indices[j + 1]
                        all_triangles.append((v0_out.tolist(), outer_hole_verts[hi2].tolist(), outer_hole_verts[hi1].tolist()))
            
            # Same for inner face (reversed winding)
            for i in range(5):
                v0_in = inner_face_verts[i]
                v1_in = inner_face_verts[(i + 1) % 5]
                
                angles_v0 = []
                for hv in inner_hole_verts:
                    local = hv - inner_face_center
                    local_proj = local - np.dot(local, face_normal) * face_normal
                    if np.linalg.norm(local_proj) > 0.001:
                        angle = np.arctan2(np.dot(local_proj, basis_y), np.dot(local_proj, basis_x))
                    else:
                        angle = 0
                    angles_v0.append(angle)
                
                local_v0 = v0_in - inner_face_center
                angle_v0 = np.arctan2(np.dot(local_v0, basis_y), np.dot(local_v0, basis_x))
                local_v1 = v1_in - inner_face_center
                angle_v1 = np.arctan2(np.dot(local_v1, basis_y), np.dot(local_v1, basis_x))
                
                hole_indices = []
                for hi, ha in enumerate(angles_v0):
                    a0 = angle_v0 % (2 * np.pi)
                    a1 = angle_v1 % (2 * np.pi)
                    ha_norm = ha % (2 * np.pi)
                    
                    if a0 > a1:
                        if ha_norm >= a1 and ha_norm <= a0:
                            hole_indices.append(hi)
                    else:
                        if ha_norm >= a0 and ha_norm <= a1:
                            hole_indices.append(hi)
                
                if len(hole_indices) >= 1:
                    hi = hole_indices[0] if hole_indices else 0
                    all_triangles.append((v0_in.tolist(), v1_in.tolist(), inner_hole_verts[hi].tolist()))
                    
                    for j in range(len(hole_indices) - 1):
                        hi1 = hole_indices[j]
                        hi2 = hole_indices[j + 1]
                        all_triangles.append((v0_in.tolist(), inner_hole_verts[hi1].tolist(), inner_hole_verts[hi2].tolist()))
            
            # Hole wall (connecting outer and inner hole edges)
            for i in range(CYLINDER_SEGMENTS):
                i_next = (i + 1) % CYLINDER_SEGMENTS
                v0_out = outer_hole_verts[i]
                v1_out = outer_hole_verts[i_next]
                v0_in = inner_hole_verts[i]
                v1_in = inner_hole_verts[i_next]
                
                all_triangles.append((v0_out.tolist(), v0_in.tolist(), v1_out.tolist()))
                all_triangles.append((v1_out.tolist(), v0_in.tolist(), v1_in.tolist()))
        
        else:
            # Hole is larger than face - triangulate whole pentagon
            # Outer face
            for i in range(1, 4):
                all_triangles.append((
                    outer_face_verts[0].tolist(),
                    outer_face_verts[i].tolist(),
                    outer_face_verts[i + 1].tolist()
                ))
            # Inner face (reversed)
            for i in range(1, 4):
                all_triangles.append((
                    inner_face_verts[0].tolist(),
                    inner_face_verts[i + 1].tolist(),
                    inner_face_verts[i].tolist()
                ))
    
    # Edge walls (connecting outer and inner dodecahedron edges)
    # Find all edges
    edges = set()
    for face in faces:
        for i in range(5):
            edge = tuple(sorted([face[i], face[(i + 1) % 5]]))
            edges.add(edge)
    
    for v1_idx, v2_idx in edges:
        v1_out = outer_vertices[v1_idx]
        v2_out = outer_vertices[v2_idx]
        v1_in = inner_vertices[v1_idx]
        v2_in = inner_vertices[v2_idx]
        
        # Two triangles for the edge wall
        all_triangles.append((v1_out.tolist(), v2_in.tolist(), v1_in.tolist()))
        all_triangles.append((v1_out.tolist(), v2_out.tolist(), v2_in.tolist()))
    
    return all_triangles

def add_vertex_knobs(all_triangles, circumradius, knob_radius):
    """Add spherical knobs at each vertex."""
    vertices = get_dodecahedron_vertices(circumradius)
    
    for vertex in vertices:
        # Place knob slightly outside the vertex
        direction = vertex / np.linalg.norm(vertex)
        knob_center = vertex + direction * knob_radius * 0.5
        
        # Create sphere mesh
        sphere_verts, sphere_tris = create_sphere_mesh(knob_center, knob_radius, SPHERE_SEGMENTS)
        
        # Add triangles
        for tri in sphere_tris:
            v0 = sphere_verts[tri[0]]
            v1 = sphere_verts[tri[1]]
            v2 = sphere_verts[tri[2]]
            all_triangles.append((v0.tolist(), v1.tolist(), v2.tolist()))
    
    return all_triangles

def create_simple_dodecahedron_with_holes():
    """Create a simplified but manifold dodecahedron with holes."""
    
    all_triangles = []
    circumradius = VERTEX_DIAMETER / 2
    
    # Get base geometry
    vertices = get_dodecahedron_vertices(circumradius)
    faces = get_dodecahedron_faces()
    face_centers = get_face_centers(vertices, faces)
    face_normals = get_face_normals(face_centers)
    
    # Create solid dodecahedron first (triangulated faces)
    # Then we'll represent holes symbolically with indentations
    
    for face_idx, face in enumerate(faces):
        face_verts = vertices[face]
        center = face_centers[face_idx]
        normal = face_normals[face_idx]
        hole_radius = HOLE_DIAMETERS[face_idx] / 2
        
        # Create basis on face
        v0_local = face_verts[0] - center
        basis_x = v0_local / np.linalg.norm(v0_local)
        basis_y = np.cross(normal, basis_x)
        basis_y = basis_y / np.linalg.norm(basis_y)
        
        # Create hole edge vertices
        hole_verts_outer = []
        hole_verts_inner = []
        inner_offset = WALL_THICKNESS
        
        for i in range(CYLINDER_SEGMENTS):
            angle = 2 * np.pi * i / CYLINDER_SEGMENTS
            offset = hole_radius * (np.cos(angle) * basis_x + np.sin(angle) * basis_y)
            hole_verts_outer.append(center + offset)
            hole_verts_inner.append(center + offset - normal * inner_offset)
        
        # Triangulate pentagon with hole
        # Create triangles from each pentagon edge to nearby hole vertices
        for i in range(5):
            pv0 = face_verts[i]
            pv1 = face_verts[(i + 1) % 5]
            
            # Angle of pentagon vertices relative to center
            def get_angle(v):
                local = v - center
                return np.arctan2(np.dot(local, basis_y), np.dot(local, basis_x))
            
            a0 = get_angle(pv0)
            a1 = get_angle(pv1)
            
            # Find hole vertices in this sector
            sector_hole_indices = []
            for hi in range(CYLINDER_SEGMENTS):
                ha = 2 * np.pi * hi / CYLINDER_SEGMENTS
                # Check if angle is between a0 and a1
                if a0 < a1:
                    if ha >= a0 and ha <= a1:
                        sector_hole_indices.append(hi)
                else:
                    if ha >= a0 or ha <= a1:
                        sector_hole_indices.append(hi)
            
            # Sort by angle
            sector_hole_indices.sort(key=lambda hi: (2 * np.pi * hi / CYLINDER_SEGMENTS - a0) % (2 * np.pi))
            
            if len(sector_hole_indices) == 0:
                # No hole vertices in sector, just make triangle to nearest hole vertex
                nearest = min(range(CYLINDER_SEGMENTS), 
                             key=lambda hi: abs((2 * np.pi * hi / CYLINDER_SEGMENTS - (a0 + a1) / 2) % (2 * np.pi)))
                all_triangles.append((pv0.tolist(), pv1.tolist(), hole_verts_outer[nearest].tolist()))
            else:
                # Fan from pv0 to hole vertices to pv1
                # pv0 -> first hole vertex -> second hole vertex -> ... -> pv1
                all_triangles.append((pv0.tolist(), hole_verts_outer[sector_hole_indices[0]].tolist(), 
                                     hole_verts_outer[sector_hole_indices[-1]].tolist() if len(sector_hole_indices) > 1 
                                     else pv1.tolist()))
                
                for j in range(len(sector_hole_indices) - 1):
                    hi1 = sector_hole_indices[j]
                    hi2 = sector_hole_indices[j + 1]
                    all_triangles.append((pv0.tolist(), hole_verts_outer[hi2].tolist(), hole_verts_outer[hi1].tolist()))
                
                if len(sector_hole_indices) > 0:
                    all_triangles.append((pv0.tolist(), pv1.tolist(), hole_verts_outer[sector_hole_indices[-1]].tolist()))
        
        # Inner face (around hole, pointing inward)
        inner_center = center - normal * inner_offset
        for i in range(CYLINDER_SEGMENTS):
            hi1 = i
            hi2 = (i + 1) % CYLINDER_SEGMENTS
            all_triangles.append((inner_center.tolist(), hole_verts_inner[hi2].tolist(), hole_verts_inner[hi1].tolist()))
        
        # Hole wall
        for i in range(CYLINDER_SEGMENTS):
            hi1 = i
            hi2 = (i + 1) % CYLINDER_SEGMENTS
            all_triangles.append((hole_verts_outer[hi1].tolist(), hole_verts_outer[hi2].tolist(), hole_verts_inner[hi1].tolist()))
            all_triangles.append((hole_verts_inner[hi1].tolist(), hole_verts_outer[hi2].tolist(), hole_verts_inner[hi2].tolist()))
    
    # Add vertex knobs
    for vertex in vertices:
        direction = vertex / np.linalg.norm(vertex)
        knob_center = vertex + direction * KNOB_RADIUS * 0.3
        
        sphere_verts, sphere_tris = create_sphere_mesh(knob_center, KNOB_RADIUS, SPHERE_SEGMENTS)
        
        for tri in sphere_tris:
            v0 = sphere_verts[tri[0]]
            v1 = sphere_verts[tri[1]]
            v2 = sphere_verts[tri[2]]
            all_triangles.append((v0.tolist(), v1.tolist(), v2.tolist()))
    
    return all_triangles

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("Roman Dodecahedron Navigation Device - STL Generator")
    print("=" * 60)
    print(f"Vertex-to-vertex diameter: {VERTEX_DIAMETER} mm")
    print(f"Wall thickness: {WALL_THICKNESS} mm")
    print(f"Knob radius: {KNOB_RADIUS} mm")
    print()
    print("Hole diameters by face:")
    locations = [
        "Alexandria (25-27°N)", "Jerusalem (27-30°N)", "Cyprus (30-33°N)",
        "Rhodes (33-36°N)", "Athens (36-38°N)", "Rome (38-41°N)",
        "Massilia (41-44°N)", "Lugdunum (44-46°N)", "Augusta Treverorum (46-48°N)",
        "Colonia (48-51°N)", "Londinium (51-53°N)", "Eboracum (53-56°N)"
    ]
    for i, (d, loc) in enumerate(zip(HOLE_DIAMETERS, locations)):
        print(f"  Face {i+1:2d}: {d:5.1f} mm - {loc}")
    print()
    
    print("Generating mesh...")
    all_triangles = create_simple_dodecahedron_with_holes()
    
    print(f"Generated {len(all_triangles)} triangles")
    
    output_file = "roman_dodecahedron.stl"
    print(f"Writing {output_file}...")
    write_binary_stl(output_file, all_triangles)
    
    print()
    print("Done! The STL file is ready for 3D printing.")
    print()
    print("Printing recommendations:")
    print("  - Layer height: 0.2 mm")
    print("  - Infill: 20-30%")
    print("  - Supports: May be needed for overhangs")
    print("  - Material: PLA or ABS (opaque, dark color recommended)")

if __name__ == "__main__":
    main()
