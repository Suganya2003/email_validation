import smtplib
import dns.resolver

# dns_cache= {}
# def resolve_mx_records(domain):
#     # Resolve MX records for the domain and store in the cache
#     if domain in dns_cache:
#         return dns_cache[domain]
#     try:
#         dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
#         dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
#         mx_records = dns.resolver.resolve(domain, 'MX')
#         mx_hosts = [str(mx.exchange) for mx in mx_records]
#         dns_cache[domain] = mx_hosts
#         return mx_hosts
#     except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
#         return []


import dns.resolver

def check_mx_records(domain):
    try:
        # Query MX records for the domain
        answers = dns.resolver.resolve(domain, 'MX')
        mx_hosts = [str(answer.exchange)[:-1] for answer in answers]
        return mx_hosts
    except dns.resolver.NXDOMAIN:
        return []
    except dns.resolver.NoAnswer:
        return []

def verify_email(email):
    # Check if the email address exists by connecting to the SMTP server
    domain = email.split('@')[1]
    mx_hosts = check_mx_records(domain)

    for mx_host in mx_hosts:
        try:
            smtp = smtplib.SMTP(timeout=30)
            smtp.connect(mx_host)
            status, _ = smtp.helo()
            if status == 250:
                smtp.mail('')
                code, _ = smtp.rcpt(email)
                if code == 250:
                    smtp.quit()
                    return True
                smtp.quit()
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            continue

    return False

# # Test email verification
# email_address = "pravina.sathish@gmail.com"
# is_valid_email = verify_email(email_address)
# print(f"Email is valid: {is_valid_email}")
