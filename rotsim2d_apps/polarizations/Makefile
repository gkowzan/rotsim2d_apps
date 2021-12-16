PYUIC = python -m PyQt5.uic.pyuic
PYS = PolarizationsUI.py AngleWidget.py

%.py: %.ui
	$(PYUIC) -o $@ $<

all: $(PYS)

clean:
	rm $(PYS)
