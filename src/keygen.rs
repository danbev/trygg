use openidconnect::core::{CoreIdTokenFields, CoreTokenResponse, CoreTokenType};
use openidconnect::{AccessToken, EmptyExtraTokenFields};
use sigstore::crypto::SigningScheme;
use sigstore::fulcio::oauth::OauthTokenProvider;
use sigstore::fulcio::{FulcioClient, TokenProvider, FULCIO_ROOT};
use std::env;
use std::fs;
use url::Url;

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    let t = &args[1];
    println!("token: {}", t);
    fs::write("token.text", t).expect("Could not write the token");
    //let tok = TokenProvider::Static(CoreTokenType::new("bajja".to_string));
    //let tp = OauthTokenProvider::default().with_issuer("https://github.com/login/oauth");
    let tp = OauthTokenProvider::default();
    //let tp = OauthTokenProvider::default().with_issuer("https://github.com/login/oauth");
    let fulcio = FulcioClient::new(Url::parse(FULCIO_ROOT).unwrap(), TokenProvider::Oauth(tp));

    if let Ok((signer, _cert)) = fulcio
        .request_cert(SigningScheme::ECDSA_P256_SHA256_ASN1)
        .await
    {
        let keypair = signer.to_sigstore_keypair().unwrap();
        let private_key_pem = keypair.private_key_to_pem().unwrap();
        fs::write("cosign.key", private_key_pem).expect("Could not write private key");
        let public_key_pem = keypair.public_key_to_pem().unwrap();
        fs::write("cosign.pub", public_key_pem).expect("Could not write public key");
    } else {
        println!("was not able to create keypair");
    }
}
