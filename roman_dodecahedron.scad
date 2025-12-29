// Roman Dodecahedron Navigation Device v1.0
// A speculative reconstruction based on archaeological artifacts
// 
// Specifications:
// - Vertex-to-vertex diameter: 80mm
// - 12 pentagonal faces with calibrated holes
// - 20 vertex knobs serving as 15mm standoffs
// - Wall thickness: 2mm

// Key parameters
vertex_diameter = 80;        // mm, vertex to vertex
wall_thickness = 2;          // mm
knob_radius = 9;             // mm, sized for 15mm standoff

// Derived parameters (regular dodecahedron geometry)
// For vertex-to-vertex diameter D, edge length a = D / 2.802
edge_length = vertex_diameter / 2.802;

// Circumradius (center to vertex)
circumradius = vertex_diameter / 2;

// Insphere radius (center to face center)
insphere_radius = edge_length * 1.114;

// Hole diameters for each face (calibrated for latitude bands)
// Face 1: Alexandria (25-27°N) - largest hole
// Face 12: Eboracum (53-56°N) - smallest hole
hole_diameters = [
    35,  // Face 1:  Alexandria (25-27°N)
    32,  // Face 2:  Jerusalem (27-30°N)
    29,  // Face 3:  Cyprus (30-33°N)
    26,  // Face 4:  Rhodes (33-36°N)
    23,  // Face 5:  Athens (36-38°N)
    20,  // Face 6:  Rome (38-41°N)
    17,  // Face 7:  Massilia (41-44°N)
    14,  // Face 8:  Lugdunum (44-46°N)
    12,  // Face 9:  Augusta Treverorum (46-48°N)
    10,  // Face 10: Colonia (48-51°N)
    8,   // Face 11: Londinium (51-53°N)
    6    // Face 12: Eboracum (53-56°N)
];

// Golden ratio (appears throughout dodecahedron geometry)
phi = (1 + sqrt(5)) / 2;

// Generate the 20 vertices of a regular dodecahedron
// Vertices are at:
// (±1, ±1, ±1)
// (0, ±1/φ, ±φ)
// (±1/φ, ±φ, 0)
// (±φ, 0, ±1/φ)
// Scaled to desired circumradius

function dodecahedron_vertices() = 
    let(scale = circumradius / sqrt(3))
    concat(
        // (±1, ±1, ±1)
        [for (i = [-1, 1], j = [-1, 1], k = [-1, 1]) [i, j, k] * scale],
        // (0, ±1/φ, ±φ)
        [for (j = [-1, 1], k = [-1, 1]) [0, j/phi, k*phi] * scale],
        // (±1/φ, ±φ, 0)
        [for (i = [-1, 1], j = [-1, 1]) [i/phi, j*phi, 0] * scale],
        // (±φ, 0, ±1/φ)
        [for (i = [-1, 1], k = [-1, 1]) [i*phi, 0, k/phi] * scale]
    );

// Face definitions (indices into vertex array)
// Each face is a pentagon defined by 5 vertex indices
dodecahedron_faces = [
    [0, 8, 9, 1, 14],
    [0, 14, 5, 17, 12],
    [0, 12, 10, 4, 8],
    [1, 9, 11, 3, 15],
    [1, 15, 7, 17, 14],
    [2, 10, 12, 17, 7],
    [2, 7, 15, 3, 13],
    [2, 13, 6, 4, 10],
    [3, 11, 16, 6, 13],
    [4, 6, 16, 19, 8],
    [5, 14, 17, 7, 15],
    [9, 8, 19, 18, 11]
];

// Calculate face center from vertex indices
function face_center(vertices, face) = 
    let(v = [for (i = face) vertices[i]])
    [for (i = [0:2]) (v[0][i] + v[1][i] + v[2][i] + v[3][i] + v[4][i]) / 5];

// Calculate face normal (pointing outward)
function face_normal(vertices, face) =
    let(c = face_center(vertices, face))
    c / norm(c);

// Main dodecahedron body (hollow)
module dodecahedron_body() {
    difference() {
        // Outer shell
        scale([circumradius, circumradius, circumradius])
            dodecahedron_unit();
        
        // Inner cavity (scaled for wall thickness)
        inner_scale = (circumradius - wall_thickness) / circumradius;
        scale([circumradius * inner_scale, circumradius * inner_scale, circumradius * inner_scale])
            dodecahedron_unit();
    }
}

// Unit dodecahedron (circumradius = 1)
module dodecahedron_unit() {
    // Create dodecahedron using hull of pentagon pyramids
    // This is a workaround since OpenSCAD doesn't have native dodecahedron
    
    // Use intersection of half-spaces defined by face planes
    scale_factor = 1 / sqrt(3);
    
    intersection_for(i = [0:11]) {
        // Get face normal direction
        rotate(face_rotations()[i])
            translate([0, 0, -50])
                cube([100, 100, 100], center = true);
    }
}

// Simplified dodecahedron using built-in polyhedron
module simple_dodecahedron(r) {
    // Vertices scaled to circumradius r
    scale_factor = r / sqrt(3);
    
    // Define vertices
    c = scale_factor;
    p = scale_factor * phi;
    q = scale_factor / phi;
    
    vertices = [
        // (±1, ±1, ±1) scaled
        [ c,  c,  c], [ c,  c, -c], [ c, -c,  c], [ c, -c, -c],
        [-c,  c,  c], [-c,  c, -c], [-c, -c,  c], [-c, -c, -c],
        // (0, ±1/φ, ±φ) scaled
        [ 0,  q,  p], [ 0,  q, -p], [ 0, -q,  p], [ 0, -q, -p],
        // (±1/φ, ±φ, 0) scaled
        [ q,  p,  0], [ q, -p,  0], [-q,  p,  0], [-q, -p,  0],
        // (±φ, 0, ±1/φ) scaled
        [ p,  0,  q], [ p,  0, -q], [-p,  0,  q], [-p,  0, -q]
    ];
    
    faces = [
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
    ];
    
    polyhedron(points = vertices, faces = faces, convexity = 2);
}

// Get face centers for hole placement
function get_face_centers(r) = 
    let(
        scale_factor = r / sqrt(3),
        c = scale_factor,
        p = scale_factor * phi,
        q = scale_factor / phi,
        vertices = [
            [ c,  c,  c], [ c,  c, -c], [ c, -c,  c], [ c, -c, -c],
            [-c,  c,  c], [-c,  c, -c], [-c, -c,  c], [-c, -c, -c],
            [ 0,  q,  p], [ 0,  q, -p], [ 0, -q,  p], [ 0, -q, -p],
            [ q,  p,  0], [ q, -p,  0], [-q,  p,  0], [-q, -p,  0],
            [ p,  0,  q], [ p,  0, -q], [-p,  0,  q], [-p,  0, -q]
        ],
        faces = [
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
    )
    [for (f = faces) 
        let(v = [for (i = f) vertices[i]])
        [(v[0][0]+v[1][0]+v[2][0]+v[3][0]+v[4][0])/5,
         (v[0][1]+v[1][1]+v[2][1]+v[3][1]+v[4][1])/5,
         (v[0][2]+v[1][2]+v[2][2]+v[3][2]+v[4][2])/5]
    ];

// Get vertices for knob placement
function get_vertices(r) = 
    let(
        scale_factor = r / sqrt(3),
        c = scale_factor,
        p = scale_factor * phi,
        q = scale_factor / phi
    )
    [
        [ c,  c,  c], [ c,  c, -c], [ c, -c,  c], [ c, -c, -c],
        [-c,  c,  c], [-c,  c, -c], [-c, -c,  c], [-c, -c, -c],
        [ 0,  q,  p], [ 0,  q, -p], [ 0, -q,  p], [ 0, -q, -p],
        [ q,  p,  0], [ q, -p,  0], [-q,  p,  0], [-q, -p,  0],
        [ p,  0,  q], [ p,  0, -q], [-p,  0,  q], [-p,  0, -q]
    ];

// Create a hole cylinder oriented toward face center
module face_hole(center, diameter) {
    dir = center / norm(center);
    
    // Calculate rotation to align cylinder with face normal
    angle = acos(dir[2]);
    axis = norm(cross([0, 0, 1], dir)) > 0.001 ? 
           cross([0, 0, 1], dir) / norm(cross([0, 0, 1], dir)) : 
           [1, 0, 0];
    
    translate(center * 0.5)
        rotate(a = angle, v = axis)
            cylinder(h = circumradius, d = diameter, center = true, $fn = 64);
}

// Main assembly
module roman_dodecahedron() {
    face_centers = get_face_centers(circumradius);
    vertices = get_vertices(circumradius);
    
    difference() {
        union() {
            // Main dodecahedron body (hollow)
            difference() {
                simple_dodecahedron(circumradius);
                simple_dodecahedron(circumradius - wall_thickness);
            }
            
            // Add vertex knobs (spheres at each vertex)
            for (v = vertices) {
                dir = v / norm(v);
                translate(v + dir * knob_radius * 0.3)
                    sphere(r = knob_radius, $fn = 32);
            }
        }
        
        // Cut holes in each face
        for (i = [0:11]) {
            face_hole(face_centers[i], hole_diameters[i]);
        }
    }
}

// Render the dodecahedron
roman_dodecahedron();

// Uncomment below to see face numbering reference
// (renders small numbered indicators at each face)
/*
module face_labels() {
    face_centers = get_face_centers(circumradius);
    for (i = [0:11]) {
        translate(face_centers[i] * 1.3)
            text(str(i+1), size = 5, halign = "center", valign = "center");
    }
}
face_labels();
*/
