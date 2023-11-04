# En OpenGL, los shaders se escriben en un 
# nuevo lenguaje de porgramacion llamado GLSL
# Graphics Library Shaders Language

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 outTexCoords;
out vec3 outNormals;

void main()
{
    outNormals = (modelMatrix * vec4(inNormals, 0.0)).xyz;
    outNormals = normalize(outNormals);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);
    outTexCoords = inTexCoords;
}
'''

fat_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float fatness;

out vec2 outTexCoords;
out vec3 outNormals;

void main()
{
    outNormals = (modelMatrix * vec4(inNormals, 0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = inPosition + (fatness/3) * outNormals;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    outTexCoords = inTexCoords;
}
'''
unlit_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 outTexCoords;
in vec3 outNormals;
out vec4 fragColor;

void main()
{
    fragColor = texture(tex, outTexCoords);
}
'''

gourad_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;


in vec2 outTexCoords;
in vec3 outNormals;
out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);
    fragColor = texture(tex, outTexCoords) * intensity;
}
'''

toon_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;


in vec2 outTexCoords;
in vec3 outNormals;
out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);

    if (intensity < 0.33)
        intensity = 0.2;
    else if (intensity <0.66)
        intensity = 0.6;
    else 
        intensity = 1.0;
    
    fragColor = texture(tex, outTexCoords) * intensity;
}
'''

shader1 = '''
#version 450 core

uniform float time;

out vec4 fragColor;

void main()
{
    
    float red = abs(sin(time));
    float green = abs(cos(time));
    float blue = abs(sin(time + 2.0));

    fragColor = vec4(red, green, blue, 1.0);
}
'''
