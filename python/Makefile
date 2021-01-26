
CROWDIN = java -jar ../crowdin/3.5.2/crowdin-cli.jar

LANGUAGES = $(patsubst locales/%/LC_MESSAGES/ptxprint.po,%,$(wildcard locales/*/LC_MESSAGES/ptxprint.po))
SRC_FILES = $(foreach l,${LANGUAGES},locales/${l}/LC_MESSAGES/ptxprint.po)
CROWDIN_FILES = $(foreach l,${LANGUAGES},locales/${l}/LC_MESSAGES/ptxprint.po)
MO_FILES = $(foreach l,${LANGUAGES},lib/ptxprint/mo/${l}/LC_MESSAGES/ptxprint.mo)

src : locales/ptxprint.pot ${SRC_FILES}
	@- echo done ${LANGUAGES}

mos : ${MO_FILES}
	@- echo done ${LANGUAGES}

locales/ptxprint.pot : lib/ptxprint/*.py lib/ptxprint/*.glade crowdin.yml
	xgettext -k_ --from-code=utf-8 -o $@ lib/ptxprint/*.py lib/ptxprint/*.glade
	$(CROWDIN) upload

define LANGRULES=
# locales/${1}/LC_MESSAGES/ptxprint.po :: locales/ptxprint.pot
#	msgmerge -U --lang=${1} $$@ $$<

# locales/${1}/LC_MESSAGES/ptxprint.po :: locales/${1}/LC_MESSAGES/ptxprint_crowdin.po
#	msgmerge -o $$@ $$@ $$<

lib/ptxprint/mo/${1}/LC_MESSAGES/ptxprint.mo : locales/${1}/LC_MESSAGES/ptxprint.po
	- msgfmt $$< -o $$@
endef

$(foreach l,${LANGUAGES},$(eval $(call LANGRULES,${l})))

${CROWDIN_FILES} : locales/ptxprint.pot download

download:
	$(CROWDIN) download
