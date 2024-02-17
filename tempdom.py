def is_disposable(domain):
    role_based_domains = ['admin', 'support', 'info', 'help', 'noreply']
    disposable_domains = load_disposable_domains()

    domain = domain.lower()

    if any(rb_domain in domain for rb_domain in role_based_domains):
        return False

    if any(disposable_domain in domain for disposable_domain in disposable_domains):
        return False

    return True


def load_disposable_domains():
    with open('disposable_domain.txt', 'r') as file:
        disposable_domains = [line.strip() for line in file]
    return disposable_domains

#print(is_disposable("gmaill.com"))
