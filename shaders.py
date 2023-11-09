# En OpenGL, los shaders se escriben en un 
# nuevo lenguaje de porgramacion llamado GLSL
# Graphics Library Shaders Language

trip_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 outTexCoords;
out vec4 fragColor;

uniform float time;

void main()
{
    vec2 uv = outTexCoords;
    
    // Calcula el factor de distorsión en función del tiempo
    float distortion = sin(time) * 0.1;
    
    // Calcula una coordenada de textura distorsionada
    vec2 distortedUV = uv + distortion * vec2(sin(uv.y * 10.0), cos(uv.x * 10.0));
    
    // Mapea la textura a la coordenada distorsionada
    vec4 color = texture(tex, distortedUV);
    
    fragColor = color;
}
'''

color_wave_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 outTexCoords;
in vec3 outNormals;
out vec4 fragColor;

uniform float time; // Tiempo

void main()
{
    float intensity = dot(outNormals, -dirLight);
    
    // Mapea la textura en función de las coordenadas de textura
    vec3 textureColor = texture(tex, outTexCoords).rgb;
    
    // Aplica una onda de colores basada en el tiempo
    vec3 waveColor = vec3(
        0.5 + 0.5 * sin(2.0 * time),
        0.5 + 0.5 * sin(1.5 * time),
        0.5 + 0.5 * sin(1.0 * time)
    );
    
    // Combina el color de la textura con el color de la onda y la intensidad de la luz
    vec3 finalColor = textureColor * intensity * waveColor;

    // Asigna el color resultante al fragmento
    fragColor = vec4(finalColor, 1.0);
}

'''

rainbow_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; // Textura del objeto

in vec2 outTexCoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    // Obtén la textura original del objeto
    vec4 texColor = texture(tex, outTexCoords);

    // Calcula el color del arcoíris en función de la posición del fragmento
    vec3 rainbowColor = vec3(
        0.5 + 0.5 * sin(0.1 * gl_FragCoord.x),
        0.5 + 0.5 * sin(0.1 * gl_FragCoord.y),
        0.5 + 0.5 * sin(0.1 * gl_FragCoord.x + gl_FragCoord.y)
    );

    // Combina la textura del objeto con el color del arcoíris
    vec3 finalColor = mix(texColor.rgb, rainbowColor, 0.5); // Puedes ajustar el factor de mezcla

    // Asigna el color combinado al fragmento
    fragColor = vec4(finalColor, 1.0);
}

'''

shader_rayX = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 outTexCoords;
out vec4 fragColor;

void main()
{
    vec4 color = texture(tex, outTexCoords);
    
    // Calcula el promedio de los componentes rojo, verde y azul
    float gray = (color.r + color.g + color.b) / 3.0;
    
    // Ajusta la opacidad y el color para crear el efecto de rayos X
    float opacity = 0.5; // Puedes ajustar este valor para controlar la intensidad del efecto
    fragColor = vec4(vec3(gray), opacity);
}

'''

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform sampler2D tex; // Textura del objeto

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

cel_shading = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 outTexCoords;
in vec3 outNormals;
out vec4 fragColor;

void main()
{
    // Obtén el color original de la textura del objeto
    vec4 texColor = texture(tex, outTexCoords);

    // Calcula la intensidad de la luz (cambia según el ángulo entre la normal y la dirección de la luz)
    float intensity = dot(outNormals, vec3(0.0, 0.0, 1.0)); // Aquí se asume que la luz viene desde arriba (cambia según la dirección de la luz)

    // Definir diferentes umbrales para lograr el efecto cel shading
    float threshold1 = 0.2;
    float threshold2 = 0.6;
    float threshold3 = 0.9;

    // Aplica los colores base dependiendo de la intensidad
    vec3 color;
    if (intensity < threshold1)
        color = vec3(0.0, 0.0, 0.0); // Sombra fuerte
    else if (intensity < threshold2)
        color = vec3(0.4, 0.4, 0.4); // Sombra media
    else if (intensity < threshold3)
        color = vec3(0.8, 0.8, 0.8); // Luz media
    else
        color = vec3(1.0, 1.0, 1.0); // Luz fuerte

    // Combina el color base con el color de la textura original
    vec3 finalColor = texColor.rgb * color;

    // Asigna el color resultante al fragmento
    fragColor = vec4(finalColor, texColor.a);
}
'''

vertices = '''
#version 450 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time; // Tiempo transcurrido

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 fragColor;

void main()
{
    outNormals = (modelMatrix * vec4(inNormals, 0.0)).xyz;
    outNormals = normalize(outNormals);

    // Deforma los vértices en función del tiempo
    vec3 pos = inPosition + vec3(
        0.1 * sin(2.0 * time),
        0.1 * cos(1.5 * time),
        0.1 * sin(1.0 * time)
    );

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    outTexCoords = inTexCoords;

    // Cambia el color en función del tiempo
    vec3 color = vec3(
        0.5 + 0.5 * sin(1.0 * time),
        0.5 + 0.5 * sin(1.5 * time),
        0.5 + 0.5 * sin(2.0 * time)
    );

    // Establece un contorno negro (borde) alrededor del objeto
    float edge = 0.02; // Ancho del contorno
    if (inTexCoords.x < edge || inTexCoords.x > 1.0 - edge || inTexCoords.y < edge || inTexCoords.y > 1.0 - edge) {
        color = vec3(0.0, 0.0, 0.0); // Color negro
    }

    fragColor = vec4(color, 1.0);
}

'''