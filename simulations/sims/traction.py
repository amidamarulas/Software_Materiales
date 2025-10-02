import numpy as np
import plotly.graph_objects as go


def simulate_tension(material):
    strain = np.linspace(0, 0.2, 200)
    stress = np.minimum(
        material.modulo_elasticidad * strain, material.resistencia_traccion
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=strain, y=stress, mode="lines", name="Esfuerzo-Deformación")
    )
    fig.update_layout(
        title=f"Curva Tracción - {material.nombre}",
        xaxis_title="Deformación",
        yaxis_title="Esfuerzo (MPa)",
    )
    return fig.to_html(), {
        "modulo_elasticidad": material.modulo_elasticidad,
        "limite_elastico": material.limite_elastico,
        "resistencia_traccion": material.resistencia_traccion,
    }
