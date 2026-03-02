import numpy as np
import matplotlib.pyplot as plt

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

def plot_gamma(freq, gamma, tag=None):
    if isinstance(gamma, dict):
        if tag is None:
            if len(gamma) != 1:
                raise ValueError("tag must be provided when gamma has multiple entries")
            tag, gamma = next(iter(gamma.items()))
        else:
            if tag not in gamma:
                raise KeyError(f"tag '{tag}' not found in gamma")
            gamma = gamma[tag]

    plt.figure()
    if tag:
        plt.suptitle(f"Gamma - {tag}")
    plt.subplot(2,1,1)
    mag = np.abs(gamma)
    mag = np.maximum(mag, np.finfo(float).tiny)
    plt.plot(freq/1e9, 20*np.log10(mag))
    plt.ylabel('|Gamma| [dB]')
    plt.grid()
    plt.subplot(2,1,2)
    plt.plot(freq/1e9, (np.angle(gamma)*180/np.pi))
    plt.ylabel('∠Gamma [deg]')
    plt.xlabel('Frecuencia [GHz]')
    plt.grid()
    plt.tight_layout()
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