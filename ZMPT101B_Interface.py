import machine
import utime
import math

volt_pin = machine.ADC(0) # POT-input on the Pico GPIO 26/ADC-0
VREF = 5.0;
SAMPLES_TO_COMPUTE_OFFSET = 100
ADC_MAX = 62200 # corresponds to the value of 5
ADC_MIN = 38200 # corresponds to value of 0
ADC_RANGE = ADC_MAX - ADC_MIN # Compute ranmge


# This function will convert the values from ADC to the
# corresponding DC voltage values
def MapADCToVolts(adcReading,adc_min = ADC_MIN,adc_max = ADC_MAX,volt_min = 0.0,volt_max = VREF):
   y = (adcReading-adc_min)/(adc_max-adc_min)*(volt_max-volt_min)+volt_min
   return y

# This function will collect 50 values from the ADC and compute
# the mean of this 50 values. This mean can be considered as the
# DC offset that needs to be removed from the measurments
def ComputeOffset():
    accumulate = 0
    print("Computing the offset...")
    for n in range(SAMPLES_TO_COMPUTE_OFFSET):
        accumulate = accumulate + volt_pin.read_u16()
        utime.sleep_us(1000)
        
    offsetSampleValue = accumulate/SAMPLES_TO_COMPUTE_OFFSET;
    offSetDCVolt = MapADCToVolts(offsetSampleValue, ADC_MIN, ADC_MAX, 0, VREF)
    return offSetDCVolt

def getRMSVoltage(frequency=50, offSetVoltage = 2.5):
    time_period = 1000000/frequency
    start_time = utime.ticks_us()
    Vsum = 0
    measure_count = 0
    while utime.ticks_diff(utime.ticks_us(), start_time) < time_period:
        current_volt = MapADCToVolts(volt_pin.read_u16()) - offSetVoltage
        Vsum = Vsum + (current_volt*current_volt)
        measure_count = measure_count + 1;
    SENSITIVITY = (VREF-offSetVoltage)/340
    Vrms = math.sqrt(Vsum/measure_count)/SENSITIVITY
    return Vrms

offSetVolt = ComputeOffset()
while True:
    Vrms = getRMSVoltage(50,offSetVolt)
    print("Vrms: ",str(Vrms))
    utime.sleep(1)
