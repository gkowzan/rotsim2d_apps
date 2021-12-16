PYUIC = python -m PyQt5.uic.pyuic
PYS = Ui_PathwaysWidget.py Ui_PlotsWidget.py Ui_WaitingTimeWindow.py

%.py: %.ui
	$(PYUIC) -o $@ $<

all: $(PYS)

clean:
	rm $(PYS)
