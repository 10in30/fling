from fling_cli import get_fling_client
from certbot.plugins import dns_common
from fling_client.api.loophost import (
    add_txt_record_txt_record_put,
    del_txt_record_txt_record_delete,
)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Loophost

    This Authenticator uses the Fling API to fulfill a dns-01 challenge on a *.fling.dev domain.
    """

    description = "Obtain certificates for a loophost account"
    ttl = 60
    fling_client = None

    def more_info(self) -> str:
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the Fling API and a GitHub token."
        )

    def _setup_credentials(self) -> None:
        self.fling_client = get_fling_client(require_auth=True)

    def _perform(
        self, domain: str, validation_domain_name: str, validation: str
    ) -> None:
        # TODO(JMC): Check that domain for match against username
        add_txt_record_txt_record_put.sync(
            client=self.fling_client,
            validation_domain_name=validation_domain_name,
            validation=validation,
            ttl=self.ttl,
        )

    def _cleanup(self, domain: str, validation_domain_name: str, validation: str) -> None:
        del_txt_record_txt_record_delete.sync(
            client=self.fling_client,
            validation_domain_name=validation_domain_name,
            validation=validation,
            ttl=self.ttl,
        )
