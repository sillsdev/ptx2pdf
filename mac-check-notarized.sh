#!/usr/bin/env bash
# $1 - dmg file
# $2 - request
teamId='3YE4W86L3G'
not_status="in progress"
for (( ; ; ))
do
	not_status=$(xcrun notarytool info --apple-id ${NOTARIZATION_USERNAME} --team-id ${teamId} --password ${NOTARIZATION_PASSWORD} "$2" | grep status | awk -F ': ' '{print $2}')
	echo "Status:${not_status}"
	if [ "${not_status}" = "In Progress" ]; then
		sleep 30
	elif [ "${not_status}" = "Invalid" ]; then
		xcrun notarytool log --apple-id ${NOTARIZATION_USERNAME} --team-id ${teamId} --password ${NOTARIZATION_PASSWORD} "$2"
		exit 1
	else
		break
	fi
done

exit_status=65
for (( ; ; ))
do
	xcrun stapler staple "$1"
	exit_status=$?
	if [ "${exit_status}" = "65" ]
	then
		echo "Waiting for stapling to complete"
		sleep 30
	else
		echo "Stapler status: ${exit_status}"
		break
	fi
done
