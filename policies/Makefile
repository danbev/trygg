license.wasm: license.rego
	./opa build -t wasm -e license/allow license.rego
	@tar -xf bundle.tar.gz /policy.wasm >/dev/null 2>&1
	@mv policy.wasm $@
	@${RM} bundle.tar.gz

test: license.rego test-license.rego
	./opa test . -v

.PHONY: clean
clean: 
	@${RM} bundle.tar.gz

