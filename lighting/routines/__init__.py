from lighting.routines.BlackoutRoutine import BlackoutRoutine
from lighting.routines.BleuRoutine import BleuRoutine
from lighting.routines.CyclingMultiRoutine import CyclingMultiRoutine
from lighting.routines.FireRoutine import FireRoutine
from lighting.routines.ModeRoutine import ModeRoutine
from lighting.routines.ModeSwitchRoutine import ModeSwitchRoutine
from lighting.routines.MultiRoutine import MultiRoutine
from lighting.routines.MushroomRoutine import MushroomRoutine
from lighting.routines.PowerGaugeRoutine import PowerGaugeRoutine
from lighting.routines.PulseRoutine import PulseRoutine
from lighting.routines.RainbowRoutine import RainbowRoutine
from lighting.routines.RandomPulseRoutine import RandomPulseRoutine
from lighting.routines.SpeedGaugeRoutine import SpeedGaugeRoutine
from lighting.routines.TimeRoutine import TimeRoutine
from lighting.routines.WaveRoutine import WaveRoutine


class _Routines(object):
    BlackoutRoutine: BlackoutRoutine
    BleuRoutine: BleuRoutine
    CyclingMultiRoutine: CyclingMultiRoutine
    FireRoutine: FireRoutine
    ModeRoutine: ModeRoutine
    ModeSwitchRoutine: ModeSwitchRoutine
    MultiRoutine: MultiRoutine
    MushroomRoutine: MushroomRoutine
    PowerGaugeRoutine: PowerGaugeRoutine
    PulseRoutine: PulseRoutine
    RainbowRoutine: RainbowRoutine
    RandomPulseRoutine: RandomPulseRoutine
    SpeedGaugeRoutine: SpeedGaugeRoutine
    TimeRoutine: TimeRoutine
    WaveRoutine: WaveRoutine


Routines = _Routines()
