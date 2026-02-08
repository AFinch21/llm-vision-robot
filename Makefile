lk-up:
	@echo "Starting local livekit server"
	docker compose --profile lk up

LK_HTTP_URL ?= http://localhost:7880
ROOM ?= my_room
IDENTITY ?= andrew
TOKEN_TTL ?= 3h

open-meet:
	@echo "Generating LiveKit token…"
	@TOKEN="$$(lk --url $(LK_HTTP_URL) token create \
		--api-key $$LIVEKIT_API_KEY \
		--api-secret $$LIVEKIT_API_SECRET \
		--identity $(IDENTITY) \
		--room $(ROOM) \
		--join \
		--valid-for $(TOKEN_TTL))"; \
	echo "$$TOKEN"