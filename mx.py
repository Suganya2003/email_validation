import threading
import queue
import dns.resolver
import dns.reversename

# Set the cache TTL (in seconds)
CACHE_TTL = 600

# Initialize a DNS resolver with caching enabled
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8']
resolver.cache = dns.resolver.Cache()


def query_dns(record_type, domain):
    try:
        # Try to resolve the record from cache first
        record_name = domain if record_type == 'MX' else f'{domain}.'
        cache_result = resolver.cache.get((record_name, record_type))
        if cache_result is not None and (dns.resolver.mtime() - cache_result.time) < CACHE_TTL:
            return True

        # Otherwise, perform a fresh DNS query
        resolver.timeout = 2
        resolver.lifetime = 2
        resolver.resolve(record_name, record_type)
        return True
    except dns.resolver.NXDOMAIN:
        # The domain does not exist
        return False
    except dns.resolver.NoAnswer:
        # No record of the requested type was found
        return False
    except dns.resolver.Timeout:
        # The query timed out
        return False
    except:
        # An unexpected error occurred
        return False


def has_valid_mx_record(domain):
    # Define a function to handle each DNS query in a separate thread
    def query_mx(results_queue):
        results_queue.put(query_dns('MX', domain))

    def query_a(results_queue):
        results_queue.put(query_dns('A', domain))

    # Start multiple threads to query the MX and A records simultaneously
    mx_queue = queue.Queue()
    a_queue = queue.Queue()
    mx_thread = threading.Thread(target=query_mx, args=(mx_queue,))
    a_thread = threading.Thread(target=query_a, args=(a_queue,))
    mx_thread.start()
    a_thread.start()

    # Wait for both threads to finish and retrieve the results from the queues
    mx_thread.join()
    a_thread.join()
    mx_result = mx_queue.get()
    a_result = a_queue.get()

    return mx_result or a_result

# print(has_valid_mx_record("qq.com"))
