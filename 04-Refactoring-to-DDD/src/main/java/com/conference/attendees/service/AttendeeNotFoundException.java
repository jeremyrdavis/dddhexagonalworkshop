package com.conference.attendees.service;

/**
 * Business exception thrown when an attendee is not found in the system.
 */
public class AttendeeNotFoundException extends RuntimeException {

    public AttendeeNotFoundException(String message) {
        super(message);
    }

    public AttendeeNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}