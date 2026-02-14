import Foundation

/**
 # ServiceDiscovery.swift
 # Project Antigravity — Phase 4
 
 Discovers the Orchestrator server on the local network
 via Bonjour/mDNS. Eliminates hardcoded IP addresses.
 
 The Orchestrator advertises itself as:
   Service Type: _antigravity._tcp
   Port: 9000
 
 Discovery flow:
   1. Start browsing for _antigravity._tcp services
   2. When service found → resolve to get IP + port
   3. Pass endpoint to TalkerClient.connect()
   4. If discovery fails after timeout → fall back to cached IP
   5. If no cached IP → delegate notifies UI to prompt manual entry
 
 Usage:
     let discovery = ServiceDiscovery()
     discovery.delegate = self
     discovery.startSearching()
 */

// MARK: - Delegate

protocol ServiceDiscoveryDelegate: AnyObject {
    /// Called when the Orchestrator is found on the network.
    func discovery(_ discovery: ServiceDiscovery, didFind host: String, port: Int)
    
    /// Called when discovery fails — UI should offer manual IP entry.
    func discoveryDidFail(_ discovery: ServiceDiscovery, reason: String)
}

// MARK: - ServiceDiscovery

class ServiceDiscovery: NSObject, ObservableObject {
    
    // ─────────────────────────────────────────────
    // Configuration
    // ─────────────────────────────────────────────
    
    private let serviceType = "_antigravity._tcp."
    private let domain = "local."
    private let timeoutSeconds: TimeInterval = 5.0
    
    // ─────────────────────────────────────────────
    // State
    // ─────────────────────────────────────────────
    
    @Published var isSearching: Bool = false
    @Published var foundHost: String? = nil
    @Published var foundPort: Int? = nil
    
    weak var delegate: ServiceDiscoveryDelegate?
    
    // ─────────────────────────────────────────────
    // Internals
    // ─────────────────────────────────────────────
    
    private var browser: NetServiceBrowser?
    private var resolving: NetService?
    private var timeoutTimer: Timer?
    
    /// UserDefaults key for caching last known endpoint.
    private let cacheKeyHost = "antigravity_last_host"
    private let cacheKeyPort = "antigravity_last_port"
    
    // MARK: - Public API
    
    /// Start searching for the Orchestrator on the local network.
    func startSearching() {
        guard !isSearching else { return }
        
        print("🔍 [Discovery] Searching for _antigravity._tcp on local network...")
        
        isSearching = true
        foundHost = nil
        foundPort = nil
        
        browser = NetServiceBrowser()
        browser?.delegate = self
        browser?.searchForServices(ofType: serviceType, inDomain: domain)
        
        // Set timeout — fall back to cached IP if discovery fails
        DispatchQueue.main.async {
            self.timeoutTimer = Timer.scheduledTimer(withTimeInterval: self.timeoutSeconds, repeats: false) { [weak self] _ in
                self?.handleTimeout()
            }
        }
    }
    
    /// Stop searching.
    func stopSearching() {
        browser?.stop()
        browser = nil
        resolving?.stop()
        resolving = nil
        timeoutTimer?.invalidate()
        timeoutTimer = nil
        isSearching = false
    }
    
    // MARK: - Cache Management
    
    /// Cache the last known good endpoint.
    func cacheEndpoint(host: String, port: Int) {
        UserDefaults.standard.set(host, forKey: cacheKeyHost)
        UserDefaults.standard.set(port, forKey: cacheKeyPort)
        print("💾 [Discovery] Cached endpoint: \(host):\(port)")
    }
    
    /// Retrieve the last known good endpoint.
    func getCachedEndpoint() -> (host: String, port: Int)? {
        guard let host = UserDefaults.standard.string(forKey: cacheKeyHost) else { return nil }
        let port = UserDefaults.standard.integer(forKey: cacheKeyPort)
        guard port > 0 else { return nil }
        return (host, port)
    }
    
    // MARK: - Timeout Handler
    
    private func handleTimeout() {
        guard isSearching else { return }
        
        print("⏰ [Discovery] Timeout after \(timeoutSeconds)s.")
        stopSearching()
        
        // Try cached endpoint
        if let cached = getCachedEndpoint() {
            print("📦 [Discovery] Using cached endpoint: \(cached.host):\(cached.port)")
            foundHost = cached.host
            foundPort = cached.port
            delegate?.discovery(self, didFind: cached.host, port: cached.port)
        } else {
            print("❌ [Discovery] No cached endpoint. Manual entry required.")
            delegate?.discoveryDidFail(self, reason: "Could not find the Orchestrator on your network. Please enter the IP address manually.")
        }
    }
}

// MARK: - NetServiceBrowserDelegate

extension ServiceDiscovery: NetServiceBrowserDelegate {
    
    func netServiceBrowser(_ browser: NetServiceBrowser, didFind service: NetService, moreComing: Bool) {
        print("🔍 [Discovery] Found service: \(service.name) — resolving...")
        
        // Stop timeout — we found something
        timeoutTimer?.invalidate()
        timeoutTimer = nil
        
        // Resolve to get IP + port
        resolving = service
        service.delegate = self
        service.resolve(withTimeout: 5.0)
    }
    
    func netServiceBrowser(_ browser: NetServiceBrowser, didNotSearch errorDict: [String: NSNumber]) {
        print("❌ [Discovery] Search failed: \(errorDict)")
        stopSearching()
        handleTimeout()
    }
}

// MARK: - NetServiceDelegate

extension ServiceDiscovery: NetServiceDelegate {
    
    func netServiceDidResolveAddress(_ sender: NetService) {
        guard let addresses = sender.addresses, !addresses.isEmpty else {
            print("⚠️ [Discovery] Service resolved but no addresses found.")
            handleTimeout()
            return
        }
        
        // Extract IP from the first valid address
        var hostname = [CChar](repeating: 0, count: Int(NI_MAXHOST))
        
        for address in addresses {
            address.withUnsafeBytes { ptr in
                guard let sockAddr = ptr.baseAddress?.assumingMemoryBound(to: sockaddr.self) else { return }
                
                // Only use IPv4 addresses
                guard sockAddr.pointee.sa_family == AF_INET else { return }
                
                if getnameinfo(sockAddr, socklen_t(address.count),
                               &hostname, socklen_t(hostname.count),
                               nil, 0, NI_NUMERICHOST) == 0 {
                    let host = String(cString: hostname)
                    let port = sender.port
                    
                    print("✅ [Discovery] Orchestrator found at \(host):\(port)")
                    
                    DispatchQueue.main.async {
                        self.foundHost = host
                        self.foundPort = port
                        self.isSearching = false
                        self.cacheEndpoint(host: host, port: port)
                        self.delegate?.discovery(self, didFind: host, port: port)
                    }
                    
                    self.stopSearching()
                }
            }
        }
    }
    
    func netService(_ sender: NetService, didNotResolve errorDict: [String: NSNumber]) {
        print("❌ [Discovery] Resolve failed: \(errorDict)")
        handleTimeout()
    }
}
