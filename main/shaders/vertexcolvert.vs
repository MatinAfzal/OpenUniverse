#version 330 core
in vec3 position;
in vec3 vertex_color;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;
void main()
{
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
    color = vertex_color;
}