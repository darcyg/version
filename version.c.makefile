
override INCLUDEPATHS += -I$(VERSION_LIB_ROOT)

.version.c: .FORCE
	$(VERSION_LIB_ROOT)/version.py $(PROJECT_NAME) c > .version.c

.PHONY: .FORCE
.FORCE:

C_SRC += .version.c

