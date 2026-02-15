energy_threshold = 400 # how loud a sound must be to count as speech.
pause_threshold = 0.6 # How long of a silence (seconds) means User has finished speaking.
phrase_threshold = 0.2 # Minimum speech duration to be considered a valid phrase
dynamic_energy_threshold = True # Automatically adjusts energy_threshold based on environment.(Quiet room → threshold goes DOWN, Noisy room → threshold goes UP)
non_speaking_duration = 0.45# Shorter trailing silence for faster phrase end