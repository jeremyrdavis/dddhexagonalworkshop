package com.conference.attendees.service;

/**
 * Business exception thrown when attempting to register an attendee
 * that already exists in the system.
 */
public class AttendeeAlreadyExistsException extends RuntimeException {

    public AttendeeAlreadyExistsException(String message) {
        super(message);
    }

    public AttendeeAlreadyExistsException(String message, Throwable cause) {
        super(message, cause);
    }
}