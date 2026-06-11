"""
optim.py — Tarea 4 (IEE3787)
Algoritmos de optimizacion para el problema de deconvolucion regularizada:
  - Descenso de Gradiente Proyectado (PGD / forward-backward)
  - ADMM (splitting de consenso con inversion exacta en Fourier)
"""

import numpy as np


def projected_gradient(y, H, prox, lam=0.02, tau=1.0, n_iter=100,
                        x0=None, clip=(0.0, 1.0), x_ref=None):
    """Descenso de gradiente proyectado regularizado.

    Iteracion:
        x <- x - tau * H^T (H x - y)    [paso de datos]
        x <- prox(x, tau*lam)            [regularizacion multiescala]
        x <- clip(x, 0, 1)              [proyeccion al rango valido]

    Condicion de estabilidad: tau <= 1 / ||H^T H|| = 1 (como max|OTF|^2 = 1).

    Parameters
    ----------
    y : ndarray 2D — imagen degradada observada
    H : BlurOperator — operador de desenfoque con metodos forward/adjoint
    prox : callable(x, thr) — operador prox de regularizacion
    lam : float — peso de regularizacion
    tau : float — tasa de descenso (paso)
    n_iter : int — numero de iteraciones
    x0 : ndarray o None — inicializacion (usa y si None)
    clip : tuple o None — rango de proyeccion
    x_ref : ndarray o None — referencia para calcular RMSE por iteracion

    Returns
    -------
    x : ndarray — imagen reconstruida
    rmse_hist : ndarray — historial de RMSE (vacio si x_ref es None)
    """
    x = np.array(y, copy=True) if x0 is None else np.array(x0, copy=True)
    rmse_hist = []
    for _ in range(n_iter):
        grad = H.adjoint(H.forward(x) - y)
        x = x - tau * grad
        x = prox(x, tau * lam)
        if clip is not None:
            x = np.clip(x, clip[0], clip[1])
        if x_ref is not None:
            rmse_hist.append(float(np.sqrt(np.mean((x - x_ref) ** 2))))
    return x, np.array(rmse_hist)


def admm(y, H, prox, lam=0.02, rho=1.0, n_iter=100,
         x0=None, clip=(0.0, 1.0), x_ref=None):
    """ADMM regularizado para  min 1/2 ||Hx - y||^2 + lam * R(x).

    Splitting de consenso (z = x):
        x <- argmin 1/2||Hx-y||^2 + rho/2||x-(z-u)||^2  [inversion en Fourier]
        z <- prox_{lam/rho}(x + u)
        u <- u + x - z

    La actualizacion de x es diagonal en Fourier:
        X = F^{-1}[ (conj(OTF)*Y + rho*F(z-u)) / (|OTF|^2 + rho) ]

    Parameters
    ----------
    y : ndarray 2D — imagen degradada observada
    H : BlurOperator — operador de desenfoque
    prox : callable(x, thr) — operador prox de regularizacion
    lam : float — peso de regularizacion
    rho : float — parametro de penalizacion ADMM
    n_iter : int — numero de iteraciones
    x0 : ndarray o None — inicializacion
    clip : tuple o None — rango valido (aplicado a z)
    x_ref : ndarray o None — referencia para RMSE

    Returns
    -------
    z : ndarray — imagen reconstruida
    rmse_hist : ndarray — historial de RMSE
    """
    Y = np.fft.fft2(y)
    denom = H.otf_abs2 + rho
    num_data = H.otf_conj * Y

    x = np.array(y, copy=True) if x0 is None else np.array(x0, copy=True)
    z = np.array(x, copy=True)
    u = np.zeros_like(x)
    rmse_hist = []
    for _ in range(n_iter):
        rhs = num_data + rho * np.fft.fft2(z - u)
        x = np.real(np.fft.ifft2(rhs / denom))
        z = prox(x + u, lam / rho)
        if clip is not None:
            z = np.clip(z, clip[0], clip[1])
        u = u + x - z
        if x_ref is not None:
            rmse_hist.append(float(np.sqrt(np.mean((z - x_ref) ** 2))))
    out = np.clip(z, clip[0], clip[1]) if clip is not None else z
    return out, np.array(rmse_hist)
