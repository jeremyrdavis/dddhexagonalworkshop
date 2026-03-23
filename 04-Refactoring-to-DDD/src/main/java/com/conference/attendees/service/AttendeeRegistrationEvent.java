package com.conference.attendees.service;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * Traditional event class using CDI events.
 * This will be refactored to a proper Domain Event later.
 */
public class AttendeeRegistrationEvent implements Serializable {

    private final String email;
    private final String fullName;
    private final LocalDateTime registrationDate;
    private final LocalDateTime eventTimestamp;

    public AttendeeRegistrationEvent(String email, String fullName, LocalDateTime registrationDate) {
        this.email = email;
        this.fullName = fullName;
        this.registrationDate = registrationDate;
        this.eventTimestamp = LocalDateTime.now();
    }

    public String getEmail() {
        return email;
    }

    public String getFullName() {
        return fullName;
    }

    public LocalDateTime getRegistrationDate() {
        return registrationDate;
    }

    public LocalDateTime getEventTimestamp() {
        return eventTimestamp;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AttendeeRegistrationEvent that = (AttendeeRegistrationEvent) o;
        return Objects.equals(email, that.email) &&
                Objects.equals(eventTimestamp, that.eventTimestamp);
    }

    @Override
    public int hashCode() {
        return Objects.hash(email, eventTimestamp);
    }

    @Override
    public String toString() {
        return "AttendeeRegistrationEvent{" +
                "email='" + email + '\'' +
                ", fullName='" + fullName + '\'' +
                ", registrationDate=" + registrationDate +
                ", eventTimestamp=" + eventTimestamp +
                '}';
    }
}