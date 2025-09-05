import numpy as np
import argparse


def add_noise(VolsperTime4D, SNR):
    """
    Add Rician noise to a 4D volume with specified SNR
    
    Parameters:
        VolsperTime4D (numpy.ndarray): 4D array of shape (x,y,z,t)
        SNR (float): Signal-to-Noise Ratio (between 0 and 100)
        
    Returns:
        numpy.ndarray: Noisy 4D array with same shape as input
    """
    # Get dimensions
    x, y, z, N = VolsperTime4D.shape
    Size = (x, y, z)
    
    # Initialize output array
    VolsperTime4Dnoise = np.zeros_like(VolsperTime4D)
    Sigs = np.zeros(N)
    
    for I in range(N):
        Img = VolsperTime4D[:, :, :, I]
        aux = Img > 0
        
        # Calculate noise standard deviation based on SNR
        Sigs[I] = np.mean(Img[aux]) / SNR
        
        # Generate Rician noise
        noise_real = Sigs[I] * np.random.randn(*Size)
        noise_imag = Sigs[I] * np.random.randn(*Size)
        
        # Add Rician noise to image
        VolsperTime4Dnoise[:, :, :, I] = np.sqrt((Img + noise_real)**2 + noise_imag**2)
    
    return VolsperTime4Dnoise

def main():
    parser = argparse.ArgumentParser(description='Read DICOM folder and display information')
    parser.add_argument('VolsperTime4D', type=str, help='Images for each time point')
    parser.add_argument('SNR', type=str, help='SNR level')
    parser.add_argument('--display', action='store_true', help='Display middle slice of each series')
    args = parser.parse_args() 
    volumes, metadata = add_noise(args.VolsperTime4D, args.SNR)    
    
if __name__ == "__main__":
    main() 