
CROWDIN = java -jar ../crowdin/3.5.2/crowding-cli.jar

LANGUAGES = $(filter-out ptxprint.%,$(notdir $(wildcard locales/*)))
SRC_FILES = $(foreach l,${LANGUAGES},locales/${l}/LC_MESSAGES/ptxprint.po)

locales/ptxprint.pot : lib/ptxprint/*.py lib/ptxprint/*.glade
	xgettext -k_ --from-code=utf-8 -o $@ lib/ptxprint/*.py lib/ptxprint/*.glade

define LANGRULES=
locales/${1}/LC_MESSAGES/ptxprint.po : locales/ptxprint.pot
	msgmerge -o $$@ $$@ $$<

lib/ptxprint/mo/${1}/LC_MESSAGES/ptxprint.mo : locales/${1}/LC_MESSAGES/ptxprint.po
	msgfmt $$< -o $$@
endef

$(foreach l,${LANGUAGES},$(eval $(call LANGRULES,${l})))

src : ${SRC_FILES}
	@- echo done ${LANGUAGES}


