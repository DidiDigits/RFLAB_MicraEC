import numpy as np
import matplotlib.pyplot as plt
import skrf as rf

def plot_error_parameters(freq, error_params_p1, error_params_p2):
    # Plot error parameters for Port 1
    plt.figure(figsize=(12, 8))
    plt.suptitle('Parámetros de Error - Puerto 1', fontsize=14, fontweight='bold')
        
    plt.subplot(3, 2, 1)
    plt.plot(freq/1e9, 20*np.log10(np.abs(error_params_p1['e00'])))
    plt.ylabel('|e00| [dB]')
    plt.grid()
        
    plt.subplot(3, 2, 2)
    plt.plot(freq/1e9, np.unwrap(np.angle(error_params_p1['e00']))*180/np.pi)
    plt.ylabel('∠e00 [deg]')
    plt.grid()
        
    plt.subplot(3, 2, 3)
    plt.plot(freq/1e9, 20*np.log10(np.abs(error_params_p1['e11'])))
    plt.ylabel('|e11| [dB]')
    plt.grid()
        
    plt.subplot(3, 2, 4)
    plt.plot(freq/1e9, np.unwrap(np.angle(error_params_p1['e11']))*180/np.pi)
    plt.ylabel('∠e11 [deg]')
    plt.grid()
        
    plt.subplot(3, 2, 5)
    plt.plot(freq/1e9, 20*np.log10(np.abs(error_params_p1['e10e01'])))
    plt.ylabel('|e10*e01| [dB]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
        
    plt.subplot(3, 2, 6)
    plt.plot(freq/1e9, np.unwrap(np.angle(error_params_p1['e10e01']))*180/np.pi)
    plt.ylabel('∠e10*e01 [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
        
    plt.tight_layout()
    plt.show(block=False)
        
    # Plot error parameters for Port 2
    plt.figure(figsize=(12, 8))
    plt.suptitle('Parámetros de Error - Puerto 2', fontsize=14, fontweight='bold')
        
    plt.subplot(3, 2, 1)
    plt.plot(freq/1e9, 20*np.log10(np.abs(error_params_p2['e33'])))
    plt.ylabel('|e33| [dB]')
    plt.grid()
        
    plt.subplot(3, 2, 2)
    plt.plot(freq/1e9, np.unwrap(np.angle(error_params_p2['e33']))*180/np.pi)
    plt.ylabel('∠e33 [deg]')
    plt.grid()
        
    plt.subplot(3, 2, 3)
    plt.plot(freq/1e9, 20*np.log10(np.abs(error_params_p2['e22'])))
    plt.ylabel('|e22| [dB]')
    plt.grid()
        
    plt.subplot(3, 2, 4)
    plt.plot(freq/1e9, np.unwrap(np.angle(error_params_p2['e22']))*180/np.pi)
    plt.ylabel('∠e22 [deg]')
    plt.grid()
        
    plt.subplot(3, 2, 5)
    plt.plot(freq/1e9, 20*np.log10(np.abs(error_params_p2['e23e32'])))
    plt.ylabel('|e23*e32| [dB]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
        
    plt.subplot(3, 2, 6)
    plt.plot(freq/1e9, np.unwrap(np.angle(error_params_p2['e23e32']))*180/np.pi)
    plt.ylabel('∠e23*e32 [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
        
    plt.tight_layout()
    plt.show(block=False)
        
    # Pause to view the plots
    input("\nPresione Enter para continuar...")

def plot_alpha(freq, alpha):
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(freq/1e9, 20*np.log10(np.abs(alpha)))
    plt.ylabel('|alpha| [dB]')
    plt.grid()

    plt.subplot(2,1,2)
    plt.plot(freq/1e9, (np.angle(alpha)*180/np.pi))
    plt.ylabel('∠alpha [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
    plt.tight_layout()
    plt.show(block=False)

    # Pause to view the plots
    input("\nPresione Enter para continuar...")

def plot_X(freq, X):
    plt.figure(figsize=(12, 8))
    plt.subplot(4,2,1)
    plt.plot(freq/1e9, 20*np.log10(np.abs(X[:, 0, 0])))
    plt.ylabel('|X[1,1]| [dB]')
    plt.grid()

    plt.subplot(4,2,2)
    plt.plot(freq/1e9, (np.angle(X[:, 0, 0])*180/np.pi))
    plt.ylabel('∠X[1,1] [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()


    plt.subplot(4,2,3)
    plt.plot(freq/1e9, 20*np.log10(np.abs(X[:, 0, 1])))
    plt.ylabel('|X[1,2]| [dB]')
    plt.grid()

    plt.subplot(4,2,4)
    plt.plot(freq/1e9, (np.angle(X[:, 0, 1])*180/np.pi))
    plt.ylabel('∠X[1,2] [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()

    plt.subplot(4,2,5)
    plt.plot(freq/1e9, 20*np.log10(np.abs(X[:, 1, 0])))
    plt.ylabel('|X[2,1]| [dB]')
    plt.grid()

    plt.subplot(4,2,6)
    plt.plot(freq/1e9, (np.angle(X[:, 1, 0])*180/np.pi))
    plt.ylabel('∠X[2,1] [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()

    plt.subplot(4,2,7)
    plt.plot(freq/1e9, 20*np.log10(np.abs(X[:, 1, 1])))
    plt.ylabel('|X[2,2]| [dB]')
    plt.grid()

    plt.subplot(4,2,8)
    plt.plot(freq/1e9, (np.angle(X[:, 1, 1])*180/np.pi))
    plt.ylabel('∠X[2,2] [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()

    plt.tight_layout()
    plt.show(block=False)

    # Pause to view the plots
    input("\nPresione Enter para continuar...")

def plot_S21n(freq, S21):
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(freq/1e9, 20*np.log10(np.abs(S21)))
    plt.ylabel('|S21| [dB]')
    plt.grid()

    plt.subplot(2,1,2)
    plt.plot(freq/1e9, (np.angle(S21)*180/np.pi))
    plt.ylabel('∠S21 [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
    plt.tight_layout()
    plt.show(block=False)

    # Pause to view the plots
    input("\nPresione Enter para continuar...")

def plot_detT(T_thru, freq):
    det = np.zeros(T_thru.shape[0])

    for k in range(T_thru.shape[0]):
        det[k] = np.linalg.det(T_thru[k])

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(freq/1e9, abs(det))
    plt.ylabel('|det(T)|')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
    plt.subplot(2,1,2)
    plt.plot(freq/1e9, (np.angle(det)*180/np.pi))
    plt.ylabel('∠det(T) [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
    plt.tight_layout()
    input("\nPresione Enter para continuar...")

def plot_tau(freq, tau):
    plt.figure()
    plt.plot(freq/1e9, tau*1e9)
    plt.ylabel('Tau [ns]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
    plt.tight_layout()
    input("\nPresione Enter para continuar...")

def plot_gamma(freq, gamma, title="Coeficiente de Reflexión (Gamma)", standard_type=None):
    """
    Plotea gamma en una carta de Smith.
    
    Parameters
    ----------
    freq : np.ndarray
        Vector de frecuencia (Hz)
    gamma : np.ndarray
        Coeficiente de reflexión complejo
    title : str
        Título del gráfico
    standard_type : str, optional
        Tipo de estándar ('SHORT', 'OPEN', 'LOAD') para identificar en la leyenda
    """
    # Crear red con los parámetros de gamma S11
    ntwk = rf.Network(frequency=freq, s=gamma.reshape(-1, 1, 1), name=title)
    
    # Plotear en carta de Smith
    fig, ax = plt.subplots(figsize=(8, 8))
    ntwk.plot_s_smith(m=0, n=0, ax=ax)
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    # Agregar leyenda si se especifica el tipo de estándar
    if standard_type:
        normalized_type = str(standard_type).strip().upper()
        colors = {'SHORT': 'red', 'OPEN': 'blue', 'LOAD': 'green'}
        color = colors.get(normalized_type, 'black')
        ax.plot([], [], 'o-', color=color, label=normalized_type, linewidth=2, markersize=8)
        ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    plt.tight_layout()
    plt.show(block=False)
    
    input("\nPresione Enter para continuar...")


def plot_multiple_gamma_smith(freq, gamma_dict, puerto=None):
    """
    Plotea múltiples valores de gamma (SHORT, OPEN, LOAD) en una sola carta de Smith.
    
    Parameters
    ----------
    freq : np.ndarray
        Vector de frecuencia (Hz)
    gamma_dict : dict
        Diccionario con claves 'SHORT', 'OPEN', 'LOAD' y valores de gamma complejos
    puerto : int, optional
        Número de puerto (1 o 2) para el título
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    colors = {'SHORT': 'red', 'OPEN': 'blue', 'LOAD': 'green'}
    
    for standard_name, gamma_values in gamma_dict.items():
        normalized_name = str(standard_name).strip().upper()
        if len(gamma_values) == len(freq):
            # Crear red para cada estándar
            ntwk = rf.Network(frequency=freq, s=gamma_values.reshape(-1, 1, 1), 
                            name=normalized_name)
            
            # Obtener los valores de S11 para plotear
            s11_complex = ntwk.s[:, 0, 0]
            
            # Plotear puntos en la carta de Smith
            ax.plot(np.real(s11_complex), np.imag(s11_complex), 
                     'o-', color=colors.get(normalized_name, 'black'), 
                     label=normalized_name, linewidth=2, markersize=4, alpha=0.7)
    
    # Dibujar la carta de Smith de fondo (no retorna nada, solo dibuja)
    rf.plotting.smith(ax=ax, draw_labels=True)
    
    title = f"Gamma - Standards (Puerto {puerto})" if puerto else "Coeficientes de Reflexión - Standards"
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.show(block=False)
    
    input("\nPresione Enter para continuar...")

def plot_gamma_in(freq, gamma_in, puerto):

    plt.figure()
    plt.plot(freq, 20 * np.log10(np.abs(gamma_in)), label=f"S{puerto}{puerto} medido")
    plt.title(f"Medición S{puerto}{puerto} (Gamma_in)")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud (dB)")
    plt.grid()  
    # Pause to view the plots
    input("\nPresione Enter para continuar...")