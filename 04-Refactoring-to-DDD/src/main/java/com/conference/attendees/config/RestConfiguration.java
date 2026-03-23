package com.conference.attendees.config;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

/**
 * JAX-RS configuration class.
 */
@ApplicationPath("/")
public class RestConfiguration extends Application {
    // This class enables JAX-RS for the entire application
}