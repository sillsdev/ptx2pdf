
CROWDIN = java -jar ../crowdin/3.6.5/crowdin-cli.jar

LANGUAGES = $(patsubst locales/%/LC_MESSAGES/ptxprint.po,%,$(wildcard locales/*/LC_MESSAGES/ptxprint.po))
SRC_FILES = $(foreach l,${LANGUAGES},locales/${l}/LC_MESSAGES/ptxprint.po)
CROWDIN_FILES = $(foreach l,${LANGUAGES},locales/${l}/LC_MESSAGES/ptxprint.po)
MO_FILES = $(foreach l,${LANGUAGES},lib/ptxprint/mo/${l}/LC_MESSAGES/ptxprint.mo)

.PHONY: download upload

all : locales/ptxprint.pot download ${MO_FILES}
	@- echo done ${LANGUAGES}

mos : ${MO_FILES}
	@- echo done ${LANGUAGES}

locales/ptxprint.pot : lib/ptxprint/*.py lib/ptxprint/ptxprint.glade crowdin.yml
	perl -CSD -pe 's/(name="name")/\1 translatable="yes"/o' lib/ptxprint/ptxprint.glade > temp.glade
	xgettext -k_ --from-code=utf-8 -o $@ lib/ptxprint/*.py temp.glade
	$(CROWDIN) upload

define LANGRULES=
lib/ptxprint/mo/${1}/LC_MESSAGES :
	mkdir -p $$@

locales/${1}/LC_MESSAGES/ptxprint.po : locales/ptxprint.pot
	msgmerge -U --lang=${1} $$@ $$<

# locales/${1}/LC_MESSAGES/ptxprint.po :: locales/${1}/LC_MESSAGES/ptxprint_crowdin.po
#	msgmerge -o $$@ $$@ $$<


lib/ptxprint/mo/${1}/LC_MESSAGES/ptxprint.mo : locales/${1}/LC_MESSAGES/ptxprint.po
	@mkdir -p lib/ptxprint/mo/${1}/LC_MESSAGES
	- msgfmt $$< -o $$@
endef

$(foreach l,${LANGUAGES},$(eval $(call LANGRULES,${l})))

download:
	$(CROWDIN) download

# Push the local .po files up to Crowdin as translations. This deliberately has NO prerequisites and never
# runs "download" (or the .pot/xgettext rule): Crowdin must receive what is on disk, not replace it.
# --auto-approve-imported makes the uploaded text the approved translation, so a later "make download"
# returns it. Override with: make upload CROWDIN_UPLOAD_OPTS=
CROWDIN_UPLOAD_OPTS ?= --auto-approve-imported

upload:
	$(CROWDIN) upload translations $(CROWDIN_UPLOAD_OPTS)
